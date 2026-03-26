# Конфигурация бота
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

# GitHub
GITHUB_REPO = os.getenv('GITHUB_REPO', 'kimiclawai/islamic-finance-knowledge-base')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Настройки
KNOWLEDGE_REFRESH_INTERVAL = int(os.getenv('KNOWLEDGE_REFRESH_INTERVAL', '3600'))
MAX_MESSAGE_LENGTH = 4096
CONTEXT_WINDOW = 10

# Дисклеймер
DISCLAIMER = """⚠️ <b>Важно!</b>

Я — ИИ-ассистент, предоставляющий <b>информацию</b> об исламских финансах и исламском праве.

❌ <b>Я не выдаю фатвы</b> (религиозные заключения).

✅ Для религиозно-значимых решений обращайтесь к квалифицированным учёным (муфтиям).

<b>Как я могу помочь:</b>
• Объяснить концепции исламских финансов
• Рассказать о контрактах (мурабаха, иджара и т.д.)
• Дать информацию о регуляторных стандартах
• Сравнить продукты
• Помочь с глоссарием

Нажмите /help для списка команд.
"""

# Промпты
SYSTEM_PROMPT = """Ты — ИИ-консультант по исламским финансам и исламскому праву.

КРИТИЧЕСКИ ВАЖНЫЕ ПРАВИЛА:
1. Ты НЕ выдаёшь фатвы (религиозные заключения).
2. Для религиозно-значимых решений всегда направляй к муфтиям.
3. Используй предоставленную базу знаний.
4. Отвечай точно, но доступно.
5. Указывай источники информации.

Твоя цель — образование, а не замена учёным.
"""

# Пути
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
KNOWLEDGE_FILE = os.path.join(DATA_DIR, 'knowledge_base.json')
