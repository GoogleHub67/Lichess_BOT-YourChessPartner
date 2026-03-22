import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    LICHESS_TOKEN: str = os.getenv("LICHESS_TOKEN", "YOUR_TOKEN_HERE")
    STOCKFISH_PATH: str = r"C:\Users\Aarav\OneDrive\Documents\Codes\pythonCodes\Chess\Stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
    FAIRY_STOCKFISH_PATH: str = r"C:\Users\Aarav\OneDrive\Documents\Codes\pythonCodes\Chess\Lichess Bot\fairy-stockfish-largeboard_x86-64.exe"

    CPL_MIN_SAMPLES: int = 3
    DEFAULT_ELO: int = 1320

    CPL_ELO_MAP: list[tuple[int, int]] = [
        (15,  2200),
        (25,  2000),
        (40,  1800),
        (60,  1600),
        (90,  1400),
        (130, 1320),
        (999, 1320),
    ]

    ACCEPT_VARIANTS: list[str] = ["standard", "chess960"]
    ACCEPT_TIME_CONTROLS: list[str] = ["bullet", "blitz", "rapid", "classical", "correspondence"]
    DECLINE_RATED: bool = False

    CHAT_GREET: str = "Hi! I'm YourChessPartner - I'll adapt to your level. Good luck!"
    CHAT_GG: str = "Good game! Review your moves - that's how you improve."
    CHAT_BLUNDER_DETECTED: str = "Ooof. Big blunder there!"
