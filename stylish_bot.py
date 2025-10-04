from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔑 КОНФИГУРАЦИЯ (ЗАМЕНИ ЭТИ ЗНАЧЕНИЯ!)
TELEGRAM_TOKEN = "7945400830:AAHqPnOUwiFy3ntyhWh8Uila7Ut3O3MHdUQ"  # Твой токен бота
VERCEL_URL = "https://fenix-ai-bot-tau.vercel.app"  # Замени на свой Vercel URL
GITHUB_REPO = "https://github.com/v9276556-svg"  # Замени на свой GitHub репозиторий

app = Flask(__name__)

# Инициализация бота
application = Application.builder().token(TELEGRAM_TOKEN).build()

# 📊 Хранилище данных (в памяти)
user_data = {}

# 🎨 КЛАВИАТУРЫ
def main_menu_keyboard():
    """Главное меню с кнопками"""
    keyboard = [
        [InlineKeyboardButton("🚀 Функции", callback_data="features")],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton("💡 Помощь", callback_data="help")],
        [InlineKeyboardButton("🌐 Ссылки", callback_data="links")]
    ]
    return InlineKeyboardMarkup(keyboard)

def features_keyboard():
    """Кнопки функций"""
    keyboard = [
        [InlineKeyboardButton("📝 Создать заметку", callback_data="create_note")],
        [InlineKeyboardButton("🎯 Задачи", callback_data="tasks")],
        [InlineKeyboardButton("📅 Календарь", callback_data="calendar")],
        [InlineKeyboardButton("📊 Аналитика", callback_data="analytics")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def links_keyboard():
    """Кнопки ссылок"""
    keyboard = [
        [InlineKeyboardButton("🌐 Vercel Приложение", url=VERCEL_URL)],
        [InlineKeyboardButton("💻 GitHub Репозиторий", url=GITHUB_REPO)],
        [InlineKeyboardButton("📚 Документация", url="https://core.telegram.org/bots/api")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def settings_keyboard():
    """Кнопки настроек"""
    keyboard = [
        [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton("🔔 Уведомления", callback_data="notifications")],
        [InlineKeyboardButton("🎨 Тема", callback_data="theme")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# 🌐 FLASK ROUTES
@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "service": "Fenix AI Bot",
        "deployment": "Vercel",
        "version": "2.0.0",
        "features": ["telegram_bot", "web_app", "api"]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "bot": "active"})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для Telegram"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            update = Update.de_json(data, application.bot)
            application.process_update(update)
            return jsonify({"status": "success"})
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return jsonify({"error": str(e)}), 400
    return jsonify({"status": "method not allowed"}), 405

# 💬 TELEGRAM HANDLERS
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Сохраняем пользователя
    user_data[chat_id] = {
        "name": user.first_name,
        "username": user.username,
        "start_count": user_data.get(chat_id, {}).get("start_count", 0) + 1
    }
    
    welcome_text = (
        f"✨ *Добро пожаловать, {user.first_name}!* ✨\n\n"
        f"🤖 *Fenix AI Assistant* - твой умный помощник\n\n"
        f"🎯 *Возможности:*\n"
        f"• Управление задачами\n"
        f"• Создание заметок\n"
        f"• Аналитика и статистика\n"
        f"• Гибкие настройки\n\n"
        f"🚀 *Развернуто на:* Vercel\n"
        f"💡 *Статус:* 24/7 онлайн\n\n"
        f"*Выбери действие в меню ниже:* 👇"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    help_text = (
        "📖 *Помощь по боту*\n\n"
        "*Основные команды:*\n"
        "/start - Запуск бота\n"
        "/help - Эта справка\n"
        "/status - Статус системы\n"
        "/menu - Главное меню\n\n"
        "*Управление:*\n"
        "Используй кнопки меню для навигации\n"
        "Все данные сохраняются автоматически\n\n"
        "*Техподдержка:*\n"
        "Проблемы? Используй /menu для возврата"
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status"""
    status_text = (
        "📊 *Статус системы*\n\n"
        "🟢 *Бот:* Активен\n"
        "🟢 *API:* Работает\n"
        "🟢 *База данных:* В памяти\n"
        "🟢 *Хостинг:* Vercel\n\n"
        "💡 *Статистика:*\n"
        f"Пользователей: {len(user_data)}\n"
        "Версия: 2.0.0\n\n"
        "🚀 Все системы работают нормально!"
    )
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /menu"""
    await update.message.reply_text(
        "🎮 *Главное меню*\n\nВыбери раздел:",
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard()
    )

# 🔘 CALLBACK HANDLERS
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий кнопок"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user = query.from_user
    
    if data == "features":
        await query.edit_message_text(
            "🚀 *Доступные функции*\n\nВыбери действие:",
            parse_mode='Markdown',
            reply_markup=features_keyboard()
        )
    
    elif data == "status":
        user_count = user_data.get(query.message.chat_id, {}).get("start_count", 1)
        status_msg = (
            f"📈 *Персональная статистика*\n\n"
            f"👤 *Пользователь:* {user.first_name}\n"
            f"🆔 *ID:* `{user.id}`\n"
            f"🎯 *Запусков:* {user_count}\n"
            f"💾 *Память:* {len(user_data)} пользователей\n\n"
            f"🌐 *Система:*\n"
            f"• Бот: 🟢 Активен\n"
            f"• Vercel: 🟢 Онлайн\n"
            f"• GitHub: 🟢 Синхронизирован"
        )
        await query.edit_message_text(status_msg, parse_mode='Markdown', reply_markup=main_menu_keyboard())
    
    elif data == "settings":
        await query.edit_message_text(
            "⚙️ *Настройки*\n\nВыбери раздел:",
            parse_mode='Markdown',
            reply_markup=settings_keyboard()
        )
    
    elif data == "help":
        help_msg = (
            "💡 *Помощь и поддержка*\n\n"
            "*Основные функции:*\n"
            "• Создание заметок и задач\n"
            "• Просмотр статистики\n"
            "• Настройка профиля\n"
            "• Управление через кнопки\n\n"
            "*Техническая информация:*\n"
            f"• Vercel: {VERCEL_URL}\n"
            f"• GitHub: {GITHUB_REPO}\n\n"
            "🔄 Используй кнопки для навигации"
        )
        await query.edit_message_text(help_msg, parse_mode='Markdown', reply_markup=main_menu_keyboard())
    
    elif data == "links":
        await query.edit_message_text(
            "🌐 *Полезные ссылки*\n\nБыстрый доступ к ресурсам:",
            parse_mode='Markdown',
            reply_markup=links_keyboard()
        )
    
    elif data == "create_note":
        await query.edit_message_text(
            "📝 *Создание заметки*\n\n"
            "Эта функция в разработке 🛠\n\n"
            "Скоро ты сможешь создавать и сохранять заметки!",
            parse_mode='Markdown',
            reply_markup=features_keyboard()
        )
    
    elif data == "tasks":
        await query.edit_message_text(
            "🎯 *Управление задачами*\n\n"
            "Раздел в разработке 🛠\n\n"
            "Скоро появится система задач и напоминаний!",
            parse_mode='Markdown',
            reply_markup=features_keyboard()
        )
    
    elif data == "profile":
        user_info = user_data.get(query.message.chat_id, {})
        profile_msg = (
            f"👤 *Профиль пользователя*\n\n"
            f"*Имя:* {user.first_name}\n"
            f"*Username:* @{user.username or 'не установлен'}\n"
            f"*User ID:* `{user.id}`\n"
            f"*Запусков бота:* {user_info.get('start_count', 1)}\n"
            f"*Чат ID:* `{query.message.chat_id}`\n\n"
            f"💾 Данные хранятся в памяти"
        )
        await query.edit_message_text(profile_msg, parse_mode='Markdown', reply_markup=settings_keyboard())
    
    elif data in ["back_main", "menu"]:
        await query.edit_message_text(
            "🎮 *Главное меню*\n\nВыбери раздел:",
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard()
        )
    
    else:
        await query.edit_message_text(
            "🔄 Возвращаю в главное меню:",
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard()
        )

# 🚀 ЗАПУСК БОТА
def setup_handlers():
    """Настройка обработчиков"""
    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("menu", menu_command))
    
    # Обработчики кнопок
    application.add_handler(CallbackQueryHandler(button_handler))

def main():
    """Основная функция"""
    print("🤖 Запуск Stylish Telegram Bot...")
    print(f"🌐 Vercel URL: {VERCEL_URL}")
    print(f"💻 GitHub: {GITHUB_REPO}")
    print("🚀 Бот готов к работе!")
    
    setup_handlers()
    
    # Для локального тестирования
    application.run_polling()

if __name__ == '__main__':
    main()
