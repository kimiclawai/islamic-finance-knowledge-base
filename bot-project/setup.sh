#!/bin/bash

echo "🤖 Islamic Finance Bot — Установка"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

echo "✓ Python найден"

# Check if .env exists
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo ""
        echo "⚠️  Создан файл .env"
        echo "📝 ОТКРОЙТЕ .env И ВСТАВЬТЕ ВАШИ ТОКЕНЫ!"
        echo ""
        echo "Инструкция: смотри QUICKSTART.md"
        exit 0
    fi
fi

# Install dependencies
echo ""
echo "📥 Установка зависимостей..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Ошибка установки. Попробуйте: pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "✅ Установка завершена!"
echo ""
echo "Запуск бота..."
python3 src/bot.py
