import asyncio
import json
import logging
import chess
import chess.engine
import httpx
from config import Config
from skill_estimator import SkillEstimator

log = logging.getLogger(__name__)
BASE_URL = "https://lichess.org"


class GameHandler:
    def __init__(self, game_id: str, token: str):
        self.game_id = game_id
        self.token = token
        self.headers = {"Authorization": f"Bearer {token}"}
        self.board = chess.Board()
        self.our_color: chess.Color | None = None
        self.engine: chess.engine.SimpleEngine | None = None
        self.estimator: SkillEstimator | None = None
        self.variant: str = "standard"

    async def run(self):
        async with httpx.AsyncClient(base_url=BASE_URL, headers=self.headers, timeout=60) as client:
            self.client = client
            try:
                async with client.stream("GET", f"/api/bot/game/stream/{self.game_id}") as resp:
                    async for line in resp.aiter_lines():
                        if line.strip():
                            event = json.loads(line)
                            await self._handle_game_event(event)
            finally:
                await self._stop_engine()

    async def _handle_game_event(self, event: dict):
        etype = event.get("type")
        if etype == "gameFull":
            self.variant = event.get("variant", {}).get("key", "standard")
            await self._start_engine(self.variant)

            me = (await self.client.get("/api/account")).json()["id"]
            white_id = event["white"].get("id", "")
            self.our_color = chess.WHITE if white_id == me else chess.BLACK
            self.estimator = SkillEstimator(self.engine, self.our_color)
            log.info(f"Playing as {'White' if self.our_color == chess.WHITE else 'Black'} | Variant: {self.variant}")
            await self._chat(Config.CHAT_GREET)
            await self._apply_state(event.get("state", {}))
        elif etype == "gameState":
            await self._apply_state(event)
            if event.get("bdraw") or event.get("wdraw"):
                await self._handle_draw_offer()
            if event.get("btakeback") or event.get("wtakeback"):
                await self._handle_takeback_offer()
            await self._handle_resign()

    async def _handle_draw_offer(self):
        try:
            info = self.engine.analyse(self.board, chess.engine.Limit(depth=8))
            score = info["score"].pov(self.our_color)
            if score.is_mate() and score.mate() < 0:
                await self.client.post(f"/api/bot/game/{self.game_id}/draw/yes")
                await self._chat("I'll take the draw.")
            elif not score.is_mate() and score.score() <= 50:
                await self.client.post(f"/api/bot/game/{self.game_id}/draw/yes")
                await self._chat("Fair enough, draw accepted.")
            else:
                await self.client.post(f"/api/bot/game/{self.game_id}/draw/no")
                await self._chat("No draws! Keep playing.")
        except Exception as e:
            log.warning(f"Draw handling failed: {e}")

    async def _handle_takeback_offer(self):
        try:
            await self.client.post(f"/api/bot/game/{self.game_id}/takeback/yes")
            await self._chat("Takeback granted!")
        except Exception as e:
            log.warning(f"Takeback failed: {e}")

    async def _handle_resign(self):
        try:
            info = self.engine.analyse(self.board, chess.engine.Limit(depth=8))
            score = info["score"].pov(self.our_color)
            if score.is_mate() and score.mate() < 0 and abs(score.mate()) <= 3:
                await self.client.post(f"/api/bot/game/{self.game_id}/resign")
                await self._chat("GG, you got me.")
        except Exception as e:
            log.warning(f"Resign failed: {e}")

    async def _apply_state(self, state: dict):
        if state.get("status", "started") not in ("started", "created"):
            await self._chat(Config.CHAT_GG)
            return
        self.board = chess.Board()
        moves_str = state.get("moves", "").strip()
        if moves_str:
            for uci in moves_str.split():
                self.board.push_uci(uci)
        if self.board.turn == self.our_color:
            await self._make_move(state)

    async def _make_move(self, state: dict):
        if self.estimator:
            self.estimator.record_opponent_move(self.board)
        elo = self.estimator.get_elo() if self.estimator else Config.DEFAULT_ELO
        move = await self._stockfish_move(elo, state)

        if move and self.board.is_legal(move):
            if self.estimator:
                board_copy = self.board.copy()
                board_copy.push(move)
                self.estimator.record_position_before_opponent_move(board_copy)
            await self._send_move(move.uci())
        else:
            log.error(f"Illegal/null move: {move}")

    async def _stockfish_move(self, elo: int, state: dict) -> chess.Move | None:
        try:
            self.engine.configure({
                "UCI_LimitStrength": True,
                "UCI_Elo": elo
            })

            wtime = state.get("wtime", 0)
            btime = state.get("btime", 0)
            if wtime == 0 and btime == 0:
                limit = chess.engine.Limit(depth=8)
            else:
                limit = chess.engine.Limit(
                    white_clock=wtime / 1000,
                    black_clock=btime / 1000,
                    white_inc=state.get("winc", 0) / 1000,
                    black_inc=state.get("binc", 0) / 1000,
                )

            result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.engine.play(self.board, limit)
            )
            log.info(f"Stockfish ELO {elo}: {result.move.uci()}")
            return result.move
        except Exception as e:
            log.error(f"Stockfish error: {e}")
            return None

    async def _send_move(self, uci: str):
        r = await self.client.post(f"/api/bot/game/{self.game_id}/move/{uci}")
        r.raise_for_status()
        log.info(f"Sent: {uci}")

    async def _chat(self, message: str, room: str = "player"):
        try:
            await self.client.post(
                f"/api/bot/game/{self.game_id}/chat",
                data={"room": room, "text": message}
            )
        except Exception as e:
            log.warning(f"Chat failed: {e}")

    async def _start_engine(self, variant: str = "standard"):
        path = Config.FAIRY_STOCKFISH_PATH if variant == "chess960" else Config.STOCKFISH_PATH
        loop = asyncio.get_event_loop()
        self.engine = await loop.run_in_executor(
            None, lambda: chess.engine.SimpleEngine.popen_uci(path)
        )
        log.info(f"Engine started: {'Fairy-Stockfish' if variant == 'chess960' else 'Stockfish'}")

    async def _stop_engine(self):
        if self.engine:
            try:
                self.engine.quit()
            except Exception:
                pass
