import os
import sys
import subprocess
import platform

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

system = platform.system()

print("Installing Python dependencies...")
run(f"{sys.executable} -m pip install chess httpx python-dotenv")

print("\nInstalling Stockfish...")
if system == "Windows":
    run('powershell -Command "winget install --id=Stockfish.Stockfish -e"')
elif system == "Darwin":
    run("brew install stockfish")
elif system == "Linux":
    run("sudo apt install stockfish -y")

print("\nSetup complete!")
print("1. Create a .env file with: LICHESS_TOKEN=your_token")
print("2. Download a .bin opening book and set BOOK_PATH in config.py")
print("3. Run: python bot.py")