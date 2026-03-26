# 🤖 Islamic Finance AI Consultant — Telegram Bot

## Описание проекта

ИИ-консультант в Telegram, специализирующийся на исламских финансах и исламском праве. Бот использует созданную базу знаний для ответов на вопросы.

---

## Архитектура

```
User → Telegram → Bot → OpenAI API + Knowledge Base → Response
```

### Компоненты

1. **Telegram Bot** — интерфейс общения
2. **Knowledge Base Loader** — загрузка базы знаний с GitHub
3. **Context Manager** — управление контекстом разговора
4. **AI Engine** — генерация ответов на основе знаний
5. **Safety Filter** — проверка на шариатскую точность

---

## Функциональность

### Основные возможности

- 💬 **Ответы на вопросы** по исламским финансам
- 📚 **Поиск по базе знаний** — конкретные термины, контракты
- 🔍 **Объяснение концепций** — простым языком
- ⚖️ **Сравнение продуктов** — исламские vs конвенциональные
- 🌍 **Региональная специфика** — Пакистан, Малайзия, GCC, Россия
- 📖 **Глоссарий** — термины на 3 языках

### Режимы работы

1. **Consultant Mode** — консультации по продуктам
2. **Learning Mode** — обучение основам
3. **Fatwa Info Mode** — информация о фатвах (без выдачи фатв!)
4. **Comparative Mode** — сравнительный анализ

---

## Дисклеймер (Критически важно!)

⚠️ **Бот не выдаёт фатвы!**

В начале каждого разговора бот должен сообщать:

> "Я ИИ-ассистент, предоставляющий информацию об исламских финансах. Для религиозно-значимых решений (фатв) обращайтесь к квалифицированным учёным (муфтиям)."

---

## Структура проекта

```
islamic-finance-bot/
├── src/
│   ├── bot.py                 # Основной файл бота
│   ├── knowledge_loader.py    # Загрузка базы знаний
│   ├── context_manager.py     # Управление контекстом
│   ├── response_generator.py  # Генерация ответов
│   └── safety_filter.py       # Проверка безопасности
├── data/
│   └── knowledge_base.json    # Локальная копия базы
├── docs/
│   └── prompts.md             # Промпты для AI
├── config.py                  # Конфигурация
├── requirements.txt           # Зависимости
└── README.md                  # Документация
```

---

## Требования

### API Keys
- **Telegram Bot Token** — от @BotFather
- **OpenAI API Key** — от platform.openai.com
- **Optional: GitHub Token** — для авто-обновления базы

### Зависимости
```
python-telegram-bot==20.7
openai==1.0.0
requests==2.31.0
python-dotenv==1.0.0
```

---

## Установка

### 1. Клонирование

```bash
git clone https://github.com/kimiclawai/islamic-finance-knowledge-base.git
cd islamic-finance-bot
```

### 2. Создание окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создай файл `.env`:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
GITHUB_REPO=kimiclawai/islamic-finance-knowledge-base
KNOWLEDGE_REFRESH_INTERVAL=3600  # секунды
```

### 5. Запуск

```bash
python src/bot.py
```

---

## Развёртывание

### Вариант 1: VPS/Сервер

```bash
# Systemd service
sudo nano /etc/systemd/system/islamic-finance-bot.service
```

```ini
[Unit]
Description=Islamic Finance Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/islamic-finance-bot
Environment=PATH=/home/ubuntu/islamic-finance-bot/venv/bin
ExecStart=/home/ubuntu/islamic-finance-bot/venv/bin/python src/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable islamic-finance-bot
sudo systemctl start islamic-finance-bot
```

### Вариант 2: Heroku

```bash
heroku create islamic-finance-bot
heroku config:set TELEGRAM_BOT_TOKEN=xxx
heroku config:set OPENAI_API_KEY=xxx
git push heroku main
```

### Вариант 3: PythonAnywhere

1. Загрузи файлы через Files
2. Настрой виртуальное окружение
3. Создай Scheduled Task для постоянной работы

---

## Команды бота

### Доступные команды

```
/start — Начать разговор + дисклеймер
/help — Показать справку
/search [запрос] — Поиск по базе знаний
/glossary [термин] — Глоссарий
/compare [продукт1] [продукт2] — Сравнение
/madhabs — Информация о школах фикха
/contracts — Список контрактов
/cases — Кейсы из стран
/about — О проекте
```

---

## Логика работы

### Обработка запроса

1. **Получение сообщения**
2. **Проверка дисклеймера** — показан ли пользователю
3. **Определение типа запроса**
   - Прямой вопрос → AI + Knowledge Base
   - Команда → Обработчик команды
   - Непонятный → Уточнение
4. **Поиск релевантных знаний**
5. **Генерация ответа**
6. **Проверка безопасности**
7. **Отправка ответа**

### Пример промпта

```
Ты — ИИ-консультант по исламским финансам. 

ВАЖНО: Ты не выдаёшь фатвы. Для религиозно-значимых решений 
направляй к квалифицированным учёным.

База знаний:
{context}

Вопрос пользователя: {question}

Ответь на основе предоставленной базы знаний. 
Если информации недостаточно, скажи об этом.
Укажи источники (разделы базы знаний).
```

---

## Безопасность и ограничения

### Запретные темы

Бот НЕ должен:
- Выдавать фатвы
- Давать инвестиционные советы
- Рекламировать конкретные банки
- Обсуждать политические конфликты

### Мониторинг

Логирование:
- Все запросы
- Ошибки
- Попытки получить фатву

---

## Развитие проекта

### Phase 1: MVP
- Базовые ответы по базе знаний
- Простые команды
- Дисклеймер

### Phase 2: Улучшения
- Voice messages
- Inline queries
- Избранное
- История диалогов

### Phase 3: Продвинутое
- Multi-language (RU, EN, AR)
- Integration with Islamic finance APIs
- Community features
- Analytics dashboard

---

## Лицензия

MIT License

---

**Создано:** Kimi Claw  
**База знаний:** https://github.com/kimiclawai/islamic-finance-knowledge-base
