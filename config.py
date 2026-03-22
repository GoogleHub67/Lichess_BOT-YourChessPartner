import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    LICHESS_TOKEN: str = os.getenv("LICHESS_TOKEN", "YOUR_TOKEN_HERE")
    STOCKFISH_PATH: str = r"C:\Users\Aarav\OneDrive\Documents\Codes\pythonCodes\Chess\Stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    BOOK_PATH: str = "gm2001.bin"
    
    CPL_DEPTH_MAP: list[tuple[int, int]] = [
            (15,   8),
            (25,   7),
            (40,   6),
            (60,   5),
            (90,   4),
            (130,  3),
            (999,  2),
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
