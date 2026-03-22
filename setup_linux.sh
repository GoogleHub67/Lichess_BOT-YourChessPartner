echo "Installing Python dependencies..."
pip install chess httpx python-dotenv

echo "Installing Stockfish..."
sudo apt install stockfish -y

echo "Setup complete!"
echo "1. Create a .env file with: LICHESS_TOKEN=your_token"
echo "2. Download a .bin opening book and set BOOK_PATH in config.py"
echo "3. Run: python bot.py"