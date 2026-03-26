"""
Islamic Finance AI Consultant — Telegram Bot
Main bot implementation
"""
import logging
import asyncio
from typing import List, Dict, Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
import openai

from config import (
    TELEGRAM_BOT_TOKEN,
    OPENAI_API_KEY,
    OPENAI_MODEL,
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

# Initialize components
openai.api_key = OPENAI_API_KEY
knowledge_loader = KnowledgeLoader()
context_manager = ContextManager()

# Track users who saw disclaimer
user_disclaimers: set = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message with disclaimer."""
    user_id = update.effective_user.id
    user_disclaimers.add(user_id)
    
    keyboard = [
        [InlineKeyboardButton("📚 Начать обучение", callback_data='learn')],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data='ask')],
        [InlineKeyboardButton("🔍 Поиск", callback_data='search')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        DISCLAIMER,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help message."""
    help_text = """📚 <b>Доступные команды:</b>

<b>Основные:</b>
/start — Начать разговор
/help — Эта справка
/search [запрос] — Поиск по базе знаний

<b>Тематические:</b>
/glossary [термин] — Глоссарий терминов
/contracts — Список исламских контрактов
/madhabs — Школы исламского права
/cases — Кейсы из разных стран
/compare — Сравнение продуктов

<b>Примеры вопросов:</b>
• "Что такое мурабаха?"
• "В чём разница между мударабой и мушаракой?"
• "Как работает Sukuk?"
• "Расскажи о пилотном проекте в России"

⚠️ Помни: я не выдаю фатвы!
"""
    await update.message.reply_text(help_text, parse_mode='HTML')


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Search knowledge base."""
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text(
            "🔍 Использование: /search [запрос]\n\n"
            "Пример: /search мурабаха"
        )
        return
    
    await update.message.reply_text(f"🔍 Ищу: <i>{query}</i>...", parse_mode='HTML')
    
    # Search in knowledge base
    results = knowledge_loader.search(query)
    
    if results:
        response = f"📚 <b>Результаты поиска:</b>\n\n"
        for i, result in enumerate(results[:5], 1):
            response += f"{i}. <b>{result['title']}</b>\n"
            response += f"{result['snippet'][:200]}...\n"
            response += f"📍 {result['source']}\n\n"
        
        if len(response) > MAX_MESSAGE_LENGTH:
            response = response[:MAX_MESSAGE_LENGTH - 3] + "..."
        
        await update.message.reply_text(response, parse_mode='HTML')
    else:
        await update.message.reply_text(
            "❌ По вашему запросу ничего не найдено.\n"
            "Попробуйте переформулировать или используйте /help"
        )


async def glossary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show glossary entry."""
    term = ' '.join(context.args)
    
    if not term:
        await update.message.reply_text(
            "📖 Использование: /glossary [термин]\n\n"
            "Примеры:\n"
            "/glossary мурабаха\n"
            "/glossary сукук\n"
            "/glossary риба"
        )
        return
    
    entry = knowledge_loader.get_glossary_entry(term)
    
    if entry:
        response = f"📖 <b>{entry['term']}</b>\n\n"
        response += f"<i>English:</i> {entry['english']}\n"
        response += f"<i>العربية:</i> {entry['arabic']}\n\n"
        response += f"{entry['definition']}"
        
        await update.message.reply_text(response, parse_mode='HTML')
    else:
        await update.message.reply_text(
            f"❌ Термин \"{term}\" не найден в глоссарии.\n"
            f"Попробуйте: мурабаха, иджара, мудараба, сукук, риба, такафул"
        )


async def contracts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show list of Islamic finance contracts."""
    contracts_text = """📋 <b>Исламские контракты:</b>

<b>Торговые:</b>
• <b>Мурабаха</b> — продажа с известной наценкой
• <b>Иджара</b> — аренда
• <b>Салам</b> — предоплатный контракт
• <b>Истисна</b> — заказное производство

<b>Партнёрские:</b>
• <b>Мудараба</b> — инвестиционное партнёрство
• <b>Мушарака</b> — совместное предприятие

<b>Прочие:</b>
• <b>Вакала</b> — доверительное управление
• <b>Кард хасан</b> — беспроцентный заём

Напишите название контракта, чтобы узнать подробности.
"""
    await update.message.reply_text(contracts_text, parse_mode='HTML')


async def madhabs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show information about schools of fiqh."""
    madhabs_text = """⚖️ <b>Школы исламского права (мазхабы):</b>

<b>Суннитские:</b>

1️⃣ <b>Ханафитский</b>
• География: Турция, Центральная Азия, Индия, Пакистан
• Особенности: Наиболее гибкий подход к современным продуктам
• Лидер: Имам Абу Ханифа

2️⃣ <b>Маликитский</b>
• География: Северная Африка, ОАЭ, Кувейт, Катар
• Особенности: Сильная традиция торгового права
• Лидер: Имам Малик

3️⃣ <b>Шафиитский</b>
• География: Малайзия, Индонезия, Египет
• Особенности: Строгий подход к условиям договоров
• Лидер: Имам аш-Шафии

4️⃣ <b>Ханбалитский</b>
• География: Саудовская Аравия, Катар
• Особенности: Наиболее консервативная школа
• Лидер: Имам Ибн Ханбаль

<b>Шиитский:</b>
• <b>Джафаритский</b> — Иран, Ирак

Разные школы могут иметь разные мнения по одним вопросам — это нормально.
"""
    await update.message.reply_text(madhabs_text, parse_mode='HTML')


async def cases_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show case studies."""
    cases_text = """🌍 <b>Кейсы исламских финансов:</b>

<b>Пакистан</b> 🇵🇰
• Полная исламизация банковской системы
• Meezan Bank — лидер рынка
• Федеральный шариатский суд

<b>Малайзия</b> 🇲🇾
• Золотой стандарт регулирования
• Shariah Advisory Council (SAC)
• Крупнейший рынок Sukuk

<b>GCC</b> 🇸🇦🇦🇪🇶🇦
• Saudi Vision 2030
• Dubai Islamic Bank (первый в мире)
• Qatar Islamic Bank

<b>Турция</b> 🇹🇷
• Katılım Bankaları (участковые банки)
• Ziraat Katılım, Albaraka Türk

<b>Индонезия</b> 🇮🇩
• Bank Syariah Indonesia (BSI)
• Зелёные Sukuk (первые в мире)

<b>Россия</b> 🇷🇺
• Пилотный проект 2023-2025
• Татарстан, Башкортостан, Чечня, Дагестан
• KazanSummit

Напишите название страны для подробностей.
"""
    await update.message.reply_text(cases_text, parse_mode='HTML')


async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Compare Islamic vs conventional products."""
    compare_text = """⚖️ <b>Сравнение: Исламские vs Конвенциональные</b>

<b>Кредиты:</b>
• Конвенциональный: Процентная ставка, фиксированная
• Исламский (Мурабаха): Наценка известна заранее

<b>Депозиты:</b>
• Конвенциональный: Гарантированный процент
• Исламский (Мудараба): Доля от прибыли, риск распределён

<b>Страхование:</b>
• Конвенциональное: Продажа риска компании
• Исламское (Takaful): Совместная гарантия участников

<b>Облигации:</b>
• Конвенциональные: Долговой инструмент
• Sukuk: Доля в реальном активе

<b>Ипотека:</b>
• Конвенциональная: Кредит под процент
• Исламская (Мушарака): Совместное владение с выкупом

Напишите конкретный продукт для детального сравнения.
"""
    await update.message.reply_text(compare_text, parse_mode='HTML')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages with AI."""
    user_id = update.effective_user.id
    
    # Check if user saw disclaimer
    if user_id not in user_disclaimers:
        await update.message.reply_text(
            "⚠️ Пожалуйста, сначала ознакомьтесь с дисклеймером:",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Начать", callback_data='start')
            ]])
        )
        return
    
    user_message = update.message.text
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action='typing'
    )
    
    try:
        # Get relevant context from knowledge base
        relevant_knowledge = knowledge_loader.get_relevant_context(user_message)
        
        # Build messages for OpenAI
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"Relevant knowledge:\n{relevant_knowledge}"},
        ]
        
        # Add conversation history
        history = context_manager.get_history(user_id)
        messages.extend(history)
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        # Get AI response
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Add disclaimer if needed
        if any(word in user_message.lower() for word in ['фатва', 'разрешено', 'запрещено', 'халяль', 'харам']):
            ai_response += "\n\n⚠️ <i>Это информационный ответ. Для религиозного заключения обратитесь к муфтию.</i>"
        
        # Save to history
        context_manager.add_message(user_id, "user", user_message)
        context_manager.add_message(user_id, "assistant", ai_response)
        
        # Send response (split if too long)
        if len(ai_response) > MAX_MESSAGE_LENGTH:
            parts = [ai_response[i:i+MAX_MESSAGE_LENGTH] 
                    for i in range(0, len(ai_response), MAX_MESSAGE_LENGTH)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='HTML')
        else:
            await update.message.reply_text(ai_response, parse_mode='HTML')
            
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при обработке запроса.\n"
            "Попробуйте переформулировать или используйте /help"
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'start':
        await start(update, context)
    elif query.data == 'learn':
        await query.message.reply_text(
            "📚 <b>Режим обучения</b>\n\n"
            "С чего начнём?\n\n"
            "• /contracts — Исламские контракты\n"
            "• /madhabs — Школы права\n"
            "• /glossary — Глоссарий терминов\n"
            "• /cases — Реальные кейсы",
            parse_mode='HTML'
        )
    elif query.data == 'ask':
        await query.message.reply_text(
            "❓ <b>Задайте вопрос!</b>\n\n"
            "Примеры:\n"
            "• Что такое мурабаха?\n"
            "• Как работает Sukuk?\n"
            "• Расскажи о пилотном проекте в России\n\n"
            "Или используйте /search для поиска по базе.",
            parse_mode='HTML'
        )
    elif query.data == 'search':
        await query.message.reply_text(
            "🔍 Используйте команду /search [запрос]\n\n"
            "Пример: /search мурабаха"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Произошла ошибка. Попробуйте позже или используйте /help"
        )


def main() -> None:
    """Start the bot."""
    # Load knowledge base
    logger.info("Loading knowledge base...")
    knowledge_loader.load()
    logger.info("Knowledge base loaded!")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("glossary", glossary_command))
    application.add_handler(CommandHandler("contracts", contracts_command))
    application.add_handler(CommandHandler("madhabs", madhabs_command))
    application.add_handler(CommandHandler("cases", cases_command))
    application.add_handler(CommandHandler("compare", compare_command))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.add_error_handler(error_handler)
    
    # Run
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
