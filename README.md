# OpeningTrainer 🤖♟️

A Lichess bot that plays perfect opening theory from a Polyglot book,
then dynamically scales its Stockfish strength to match the opponent's
live skill level (measured by centipawn loss) once theory ends.
NOTE: Based on https://github.com/lichess-bot-devs/lichess-bot (AGPL License)

## How it works
Game starts
    │
    ▼
Opening book (.bin) ──── weighted random move (varied every game)
    │
    │ (first position not in book)
    ▼
Track opponent's moves with Stockfish
    │   → compute CPL (centipawn loss) per move
    │   → rolling average CPL
    │
    ▼
Map avg CPL → Stockfish depth
    │   CPL ≤ 15  → depth 22  (master-level play)
    │   CPL ≤ 40  → depth 17  (strong club player)
    │   CPL ≤ 90  → depth 11  (casual)
    │   CPL > 130 → depth 5   (beginner)
    ▼
Play at that depth for the rest of the game

## Setup

### 1. Install dependencies
pip install -r requirements.txt

### 2. Install Stockfish
- Windows: https://stockfishchess.org/download/ → add to PATH or set STOCKFISH_PATH in config.py
- Linux: sudo apt install stockfish
- Mac: brew install stockfish

### 3. Download an opening book
Get a free Polyglot .bin book:
https://github.com/official-stockfish/books/raw/master/gm2001.bin
Recommended: gm2001.bin (GM-level weighted moves)
Put it in this folder and set BOOK_PATH in config.py.

### 4. Create a Lichess bot account
- Make a NEW Lichess account (bot accounts can't play normal games)
- Go to https://lichess.org/account/oauth/token/create
- Create a token with scope: bot:play
- Paste it in config.py as LICHESS_TOKEN

### 5. Configure config.py
LICHESS_TOKEN = "lip_xxxxxxxxxxxx"
STOCKFISH_PATH = "stockfish"  # or "C:/stockfish/stockfish.exe" on Windows
BOOK_PATH = "gm2600.bin"

### 6. Run
python bot.py

## File structure
lichess_bot/
├── bot.py              # Event stream, challenge handler
├── game_handler.py     # Per-game loop: book → Stockfish
├── skill_estimator.py  # CPL tracker, depth mapper
├── config.py           # All settings
├── requirements.txt
└── README.md

## Notes
- The account MUST be a BOT account. Bot upgrades automatically on first run.
- Once upgraded to BOT, the account cannot play as a human anymore — use a new account.
- CPL estimation needs at least 3 opponent moves off-book before kicking in.

## Features
- Auto-accepts challenges (bullet, blitz, rapid, classical, correspondence)
- Smart draw handling (accepts when losing, declines when winning)
- Auto-resigns when mated in 3 or less
- Handles multiple concurrent games
- Automatic reconnection if stream drops
- Takeback support

## Contributing
Pull requests are welcome! If you have ideas for improvements, feel free to open an issue or submit a PR. Please credit the original author (Aarav Patel) in any forks or distributions.

## Known Limitations
- Requires Stockfish installed locally
- Opening book not included (download separately)
---

**requirements.txt**
```
chess>=1.10.0
httpx>=0.27.0
