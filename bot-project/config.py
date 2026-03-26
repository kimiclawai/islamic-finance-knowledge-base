# Конфигурация бота
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Claude (Anthropic)
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022')

# GitHub
GITHUB_REPO = os.getenv('GITHUB_REPO', 'kimiclawai/islamic-finance-knowledge-base')

# Настройки
MAX_MESSAGE_LENGTH = 4096
CONTEXT_WINDOW = 5  # Уменьшили для Claude

# Дисклеймер
DISCLAIMER = """⚠️ <b>Важно!</b>

Я — ИИ-ассистент по исламским финансам.

❌ <b>Я не выдаю фатвы</b> (религиозные заключения).
✅ Для фатв обращайтесь к муфтиям.

<b>Команды:</b>
/help — справка
/search — поиск по базе
/glossary — глоссарий
/contracts — контракты

Задайте вопрос прямо в чат!"""

# Промпт для Claude
SYSTEM_PROMPT = """Ты — ИИ-консультант по исламским финансам. 

КРИТИЧЕСКИЕ ПРАВИЛА:
1. НЕ выдавай фатвы (религиозные заключения).
2. Для религиозных решений направляй к муфтиям.
3. Используй предоставленную базу знаний.
4. Отвечай кратко и по существу.
5. При сомнениях — укажи, что информация образовательная.

База знаний загружена и доступна через контекст."""
