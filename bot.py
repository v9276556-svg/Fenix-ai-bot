from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "7945400830:AAHqPnOUwiFy3ntyhWh8Uila7Ut3O3MHdUQ"
VERCEL_URL = "https://fenix-ai-bot-tau.vercel.app"

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Клавиатура с Web App кнопкой
    keyboard = [
        [InlineKeyboardButton(
            "🚀 ОТКРЫТЬ WEB APP", 
            web_app=WebAppInfo(url=VERCEL_URL)
        )],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
        [InlineKeyboardButton("💡 Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"*Добро пожаловать в Fenix AI!*\n\n"
        f"🌐 *Web App функции:*\n"
        f"• Проверка статуса API\n"
        f"• Интерактивный интерфейс\n" 
        f"• Интеграция с Vercel\n"
        f"• Управление через Web App\n\n"
        f"*Нажми кнопку ниже чтобы открыть Web App:*",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Настройка handlers
application.add_handler(CommandHandler("start", start))

if __name__ == '__main__':
    print("🤖 Бот с Web App запущен!")
    application.run_polling()
