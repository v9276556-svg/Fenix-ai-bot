from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

TOKEN = "7809988118:AAH8u5M3Yz0t7a6w5Xr5Y2Z2Z2Z2Z2Z2Z2Z2"

# Инициализируем бота
application = Application.builder().token(TOKEN).build()

@app.route('/')
def home():
    return "🤖 Fenix AI - Vercel Deployment"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Основной webhook для Telegram"""
    try:
        data = request.get_json()
        update = Update.de_json(data, application.bot)
        application.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}, 400

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Бот работает на Vercel!")

async def vercel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 *Развернуто на Vercel*\n\n"
        "✅ Стабильно 24/7\n"
        "🚀 Без туннелей\n"
        "💡 Всегда онлайн!",
        parse_mode='Markdown'
    )

# Настройка обработчиков
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("vercel", vercel))

# Для локального запуска
if __name__ == '__main__':
    app.run(debug=True)
