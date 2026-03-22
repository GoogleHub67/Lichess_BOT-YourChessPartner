import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    LICHESS_TOKEN: str = os.getenv("LICHESS_TOKEN", "YOUR_TOKEN_HERE")
    STOCKFISH_PATH: str = r"C:\Users\Aarav\OneDrive\Documents\Codes\pythonCodes\Chess\Stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    BOOK_PATH: str = "gm2001.bin"

    CPL_DEPTH_MAP: list[tuple[int, int]] = [
        (15,  14),   # was 22
        (25,  12),   # was 20
        (40,  10),   # was 17
        (60,   8),   # was 14
        (90,   6),   # was 11
        (130,  4),   # was 8
        (999,  2),   # was 5
    ]

    CPL_MIN_SAMPLES: int = 3
    DEFAULT_DEPTH: int = 12

    ACCEPT_VARIANTS: list[str] = [
        "standard", "chess960", "crazyhouse", "antichess",
        "atomic", "horde", "kingOfTheHill", "racingKings", "threeCheck"
    ]
    ACCEPT_TIME_CONTROLS: list[str] = ["bullet", "blitz", "rapid", "classical", "correspondence"]
    DECLINE_RATED: bool = False

    CHAT_GREET: str = "Hi! I'm StopBlunderingInOpeningsYouIdiot - I'll play perfect theory, then match your level. Good luck!"
    CHAT_OFF_BOOK: str = "You're out of book! Adjusting my strength to match yours now"
    CHAT_GG: str = "Good game! Review your opening moves - that's where games are won and lost"
    CHAT_BLUNDER_DETECTED: str = "Ooof. Big blunder there!"
