"""
Islamic Finance AI Consultant — Telegram Bot
Uses Claude (Anthropic) for AI responses
"""
import logging
from typing import List, Dict, Any

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from anthropic import Anthropic

from config import (
    TELEGRAM_BOT_TOKEN,
    CLAUDE_API_KEY,
    CLAUDE_MODEL,
    DISCLAIMER,
    SYSTEM_PROMPT,
    MAX_MESSAGE_LENGTH
)
from knowledge_loader import KnowledgeLoader
from context_manager import ContextManager

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize
client = Anthropic(api_key=CLAUDE_API_KEY)
knowledge_loader = KnowledgeLoader()
context_manager = ContextManager(max_history=3)

# Track users who saw disclaimer
user_disclaimers: set = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message."""
    user_id = update.effective_user.id
    user_disclaimers.add(user_id)
    await update.message.reply_text(DISCLAIMER, parse_mode='HTML')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help."""
    help_text = """📚 <b>Команды:</b>

<b>Основные:</b>
/start — начать
/help — справка
/search [запрос] — поиск по базе

<b>Тематические:</b>
/glossary [термин] — глоссарий
/contracts — контракты
/madhabs — школы права
/cases — кейсы стран

<b>Примеры вопросов:</b>
• "Что такое мурабаха?"
• "Как работает Sukuk?"
• "Расскажи о пилоте в России"

⚠️ Я не выдаю фатвы!"""
    await update.message.reply_text(help_text, parse_mode='HTML')


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search knowledge base."""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("🔍 Использование: /search [запрос]")
        return
    
    results = knowledge_loader.search(query)
    
    if results:
        response = f"📚 <b>Результаты:</b>\n\n"
        for i, result in enumerate(results[:3], 1):
            response += f"{i}. <b>{result['title']}</b>\n{result['snippet'][:150]}...\n\n"
        await update.message.reply_text(response, parse_mode='HTML')
    else:
        await update.message.reply_text("❌ Ничего не найдено. Попробуйте другие слова.")


async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show glossary entry."""
    term = ' '.join(context.args)
    
    if not term:
        await update.message.reply_text("📖 /glossary [термин]\nПример: /glossary мурабаха")
        return
    
    entry = knowledge_loader.get_glossary_entry(term)
    
    if entry:
        response = f"📖 <b>{entry['term']}</b>\n\n"
        response += f"<i>EN:</i> {entry['english']}\n"
        response += f"<i>AR:</i> {entry['arabic']}\n\n"
        response += f"{entry['definition'][:500]}"
        await update.message.reply_text(response, parse_mode='HTML')
    else:
        await update.message.reply_text(f'❌ Термин "{term}" не найден.')


async def contracts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show contracts list."""
    text = """📋 <b>Исламские контракты:</b>

<b>Торговые:</b>
• Мурабаха — продажа с наценкой
• Иджара — аренда
• Салам — предоплата
• Истисна — заказное производство

<b>Партнерские:</b>
• Мудараба — инвестпартнерство
• Мушарака — совместное предприятие

<b>Прочие:</b>
• Вакала — доверительное управление
• Кард хасан — беспроцентный заем

Напишите название для подробностей."""
    await update.message.reply_text(text, parse_mode='HTML')


async def madhabs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show madhabs info."""
    text = """⚖️ <b>Школы права (мазхабы):</b>

1️⃣ <b>Ханафитский</b> — Турция, Центральная Азия, Пакистан
2️⃣ <b>Маликитский</b> — Северная Африка, ОАЭ, Катар
3️⃣ <b>Шафиитский</b> — Малайзия, Индонезия, Египет
4️⃣ <b>Ханбалитский</b> — Саудовская Аравия

<b>Шиитский:</b>
• Джафаритский — Иран, Ирак

Разные школы = разные мнения по одним вопросам."""
    await update.message.reply_text(text, parse_mode='HTML')


async def cases_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show case studies."""
    text = """🌍 <b>Кейсы:</b>

🇵🇰 <b>Пакистан</b> — полная исламизация, Meezan Bank
🇲🇾 <b>Малайзия</b> — золотой стандарт, SAC
🇸🇦 <b>GCC</b> — Vision 2030, Dubai Islamic Bank
🇹🇷 <b>Турция</b> — Katılım Bankaları
🇮🇩 <b>Индонезия</b> — BSI, зеленые Sukuk
🇷🇺 <b>Россия</b> — пилот 2023-2025, Татарстан

Напишите страну для подробностей."""
    await update.message.reply_text(text, parse_mode='HTML')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages with Claude."""
    user_id = update.effective_user.id
    
    if user_id not in user_disclaimers:
        await update.message.reply_text("Нажмите /start для начала")
        return
    
    user_message = update.message.text
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action='typing'
    )
    
    try:
        relevant_knowledge = knowledge_loader.get_relevant_context(user_message)
        
        prompt = f"""{SYSTEM_PROMPT}

<b>База знаний (релевантная часть):</b>
{relevant_knowledge}

<b>Вопрос пользователя:</b>
{user_message}

<b>Ответь кратко и по существу.</b>"""
        
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        ai_response = message.content[0].text
        
        if any(word in user_message.lower() for word in ['фатва', 'разрешено', 'запрещено', 'халяль', 'харам']):
            ai_response += "\n\n⚠️ <i>Образовательная информация. Для фатвы обратитесь к муфтию.</i>"
        
        context_manager.add_message(user_id, "user", user_message)
        context_manager.add_message(user_id, "assistant", ai_response)
        
        if len(ai_response) > MAX_MESSAGE_LENGTH:
            parts = [ai_response[i:i+MAX_MESSAGE_LENGTH] 
                    for i in range(0, len(ai_response), MAX_MESSAGE_LENGTH)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='HTML')
        else:
            await update.message.reply_text(ai_response, parse_mode='HTML')
            
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(
            "❌ Ошибка. Попробуйте позже или используйте /help"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Error: {context.error}")


def main() -> None:
    """Start bot."""
    logger.info("Loading knowledge base...")
    knowledge_loader.load()
    logger.info("Knowledge base loaded!")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("glossary", glossary_command))
    application.add_handler(CommandHandler("contracts", contracts_command))
    application.add_handler(CommandHandler("madhabs", madhabs_command))
    application.add_handler(CommandHandler("cases", cases_command))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
