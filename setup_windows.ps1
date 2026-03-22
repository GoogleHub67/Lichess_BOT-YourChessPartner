Write-Host "Installing Python dependencies..."
pip install chess httpx python-dotenv

Write-Host "Installing Stockfish via winget..."
winget install --id=Stockfish.Stockfish -e

Write-Host "Setup complete!"
Write-Host "1. Create a .env file with: LICHESS_TOKEN=your_token"
Write-Host "2. Download a .bin opening book and set BOOK_PATH in config.py"
Write-Host "3. Run: python bot.py"