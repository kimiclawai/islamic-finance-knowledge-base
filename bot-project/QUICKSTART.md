# 🤖 Islamic Finance AI Bot — Быстрый старт

## ⚡ 3 шага до запуска

### Шаг 1: Получи токены (5 минут)

#### Telegram (3 мин):
1. Открой Telegram, найди @BotFather
2. Напиши: `/newbot`
3. Придумай имя бота (например: `IslamicFinanceConsultantBot`)
4. Скопируй **токен** (выглядит как: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Claude API (2 мин):
1. Зайди на https://console.anthropic.com
2. Зарегистрируйся (или войди)
3. Перейди в раздел "API Keys"
4. Нажми "Create Key"
5. Скопируй ключ (выглядит как: `sk-ant-api03-...`)

---

### Шаг 2: Настрой (1 минута)

1. Открой файл `.env` в этой папке
2. Вставь свои токены:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
CLAUDE_API_KEY=sk-ant-api03-твой_ключ_здесь
```

3. Сохрани файл

---

### Шаг 3: Запусти (1 минута)

**Вариант А: Через Python**

```bash
# Установи зависимости (один раз)
pip install -r requirements.txt

# Запусти бота
python src/bot.py
```

**Вариант Б: Через setup.sh**

```bash
chmod +x setup.sh
./setup.sh
```

---

## ✅ Готово!

Бот работает. Найди его в Telegram по имени, которое дал @BotFather.

---

## 💡 Как пользоваться

Просто пиши вопросы:
- "Что такое мурабаха?"
- "Как работает Sukuk?"
- "Расскажи о пилоте в России"
- "В чём разница между мударабой и мушаракой?"

**Команды:**
- `/help` — справка
- `/search [запрос]` — поиск по базе
- `/glossary [термин]` — глоссарий
- `/contracts` — список контрактов

---

## ⚠️ Важно

- Бот не выдаёт фатвы (религиозные заключения)
- Работает пока запущена программа (не закрывай терминал)
- Claude даёт $5 бесплатного кредита новым пользователям

---

## 🆘 Проблемы?

**"Invalid token"** — проверь, правильно ли скопировал токен Telegram  
**"Authentication error"** — проверь ключ Claude  
**"Module not found"** — запусти `pip install -r requirements.txt`

---

Создано с ❤️ на базе знаний: https://github.com/kimiclawai/islamic-finance-knowledge-base
