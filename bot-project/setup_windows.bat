@echo off
chcp 65001 >nul
echo.
echo 🤖 Islamic Finance Bot - Настройка Windows
echo ==========================================
echo.

IF NOT EXIST .env.example (
    echo ❌ Ошибка: файл .env.example не найден!
    echo Убедитесь, что вы запускаете этот файл из папки bot-project
    pause
    exit /b 1
)

echo 📋 Создаю файл .env...
copy .env.example .env >nul

echo.
echo ✓ Файл .env создан!
echo.
echo ==========================================
echo ТЕПЕРЬ ВВЕДИТЕ ВАШИ ТОКЕНЫ:
echo ==========================================
echo.

set /p TELEGRAM_TOKEN="Введите Telegram Bot Token (от @BotFather): "
set /p CLAUDE_KEY="Введите Claude API Key (от console.anthropic.com): "

(
echo TELEGRAM_BOT_TOKEN=%TELEGRAM_TOKEN%
echo CLAUDE_API_KEY=%CLAUDE_KEY%
echo GITHUB_REPO=kimiclawai/islamic-finance-knowledge-base
) > .env

echo.
echo ✓ Токены сохранены!
echo.
echo ==========================================
echo УСТАНОВКА ЗАВИСИМОСТЕЙ:
echo ==========================================
echo.

python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ❌ Python не найден! Установите Python с python.org
    echo При установке ОБЯЗАТЕЛЬНО поставьте галочку "Add Python to PATH"
    pause
    exit /b 1
)

echo 📥 Устанавливаю библиотеки...
pip install -r requirements.txt

IF ERRORLEVEL 1 (
    echo.
    echo ❌ Ошибка установки. Попробуйте вручную:
    echo pip install anthropic python-telegram-bot requests python-dotenv
    pause
    exit /b 1
)

echo.
echo ✓ Все библиотеки установлены!
echo.
echo ==========================================
echo 🚀 ЗАПУСК БОТА:
echo ==========================================
echo.
echo Бот запускается... Не закрывайте это окно!
echo.
echo Для остановки нажмите Ctrl+C
echo.

python src\bot.py

pause
