#!/bin/bash

# Setup script for Islamic Finance Telegram Bot

echo "🤖 Islamic Finance Bot Setup"
echo "=============================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Virtual environment created"
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_REPO=kimiclawai/islamic-finance-knowledge-base
OPENAI_MODEL=gpt-4
EOL
    echo "⚠️  Please edit .env file with your actual API keys!"
    echo ""
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Get Telegram bot token from @BotFather"
echo "3. Get OpenAI API key from platform.openai.com"
echo "4. Run: python src/bot.py"
echo ""
