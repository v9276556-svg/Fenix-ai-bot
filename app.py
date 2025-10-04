from flask import Flask, request, jsonify, render_template_string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔑 КОНФИГУРАЦИЯ
TELEGRAM_TOKEN = "7945400830:AAHqPnOUwiFy3ntyhWh8Uila7Ut3O3MHdUQ"  # Твой токен бота
VERCEL_URL = "https://fenix-ai-bot-tau.vercel.app"  # Замени на свой Vercel URL
GITHUB_REPO = "https://github.com/v9276556-svg"  # Замени на свой GitHub репозиторий

app = Flask(__name__)

# Инициализация бота
application = Application.builder().token(TELEGRAM_TOKEN).build()

# 📊 Хранилище данных
user_data = {}

# 🎨 КРАСИВЫЙ HTML ДИЗАЙН
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Fenix AI - Stylish Web App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        
        .status-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.9em;
            margin: 10px 0;
        }
        
        .content {
            padding: 40px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border-left: 5px solid #667eea;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }
        
        .feature-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
            border: 2px solid #f1f3f4;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border-color: #667eea;
        }
        
        .feature-icon {
            font-size: 3em;
            margin-bottom: 20px;
        }
        
        .feature-title {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 15px;
            color: #2d3748;
        }
        
        .btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            margin: 10px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
            font-size: 1em;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            color: white;
            text-decoration: none;
        }
        
        .btn-telegram {
            background: #0088cc;
        }
        
        .btn-github {
            background: #333;
        }
        
        .footer {
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }
        
        .api-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }
        
        .code {
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            overflow-x: auto;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .header h1 {
                font-size: 2.2em;
            }
            
            .content {
                padding: 20px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Fenix AI</h1>
            <p>Интеллектуальный ассистент нового поколения</p>
            <div class="status-badge">🚀 Статус: Активен | 💡 Версия: 2.0.0</div>
        </div>
        
        <div class="content">
            <div style="text-align: center; margin-bottom: 30px;">
                <h2 style="color: #2d3748; margin-bottom: 15px;">Добро пожаловать в Fenix AI!</h2>
                <p style="font-size: 1.1em; color: #6c757d; max-width: 600px; margin: 0 auto;">
                    Мощный Telegram бот с искусственным интеллектом, развернутый на Vercel. 
                    Всегда онлайн, всегда доступен.
                </p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ user_count }}</div>
                    <div>Активных пользователей</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <div>Время работы</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">Vercel</div>
                    <div>Платформа</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">2.0.0</div>
                    <div>Версия приложения</div>
                </div>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <div class="feature-icon">💬</div>
                    <div class="feature-title">Умный чат-бот</div>
                    <p>Интеллектуальный ассистент в Telegram с поддержкой кнопок и меню</p>
                    <a href="https://t.me/fenix_ai_test_bot" class="btn btn-telegram" target="_blank">Открыть бота</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🌐</div>
                    <div class="feature-title">Веб-интерфейс</div>
                    <p>Красивый и адаптивный веб-сайт с информацией о проекте</p>
                    <a href="{{ vercel_url }}" class="btn">Обновить страницу</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">REST API</div>
                    <p>Полноценное API для интеграции с другими сервисами</p>
                    <a href="{{ vercel_url }}/health" class="btn">Проверить API</a>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔧</div>
                    <div class="feature-title">GitHub</div>
                    <p>Открытый исходный код и автоматические деплои</p>
                    <a href="{{ github_repo }}" class="btn btn-github" target="_blank">Исходный код</a>
                </div>
            </div>
            
            <div class="api-section">
                <h3 style="color: #2d3748; margin-bottom: 20px;">🔗 API Endpoints</h3>
                <div class="code">
                    GET {{ vercel_url }}/health<br>
                    → Проверка здоровья сервиса
                </div>
                <div class="code">
                    GET {{ vercel_url }}/api/status<br>
                    → Полная статистика системы
                </div>
                <div class="code">
                    POST {{ vercel_url }}/webhook<br>
                    → Webhook для Telegram бота
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <h3 style="color: #2d3748; margin-bottom: 20px;">🚀 Быстрый старт</h3>
                <a href="https://t.me/fenix_ai_test_bot?start=web" class="btn btn-telegram">Начать общение с ботом</a>
                <a href="{{ vercel_url }}/status" class="btn">Статус системы</a>
                <a href="https://core.telegram.org/bots/api" class="btn" target="_blank">Документация</a>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 Fenix AI Assistant. Все права защищены.</p>
            <p>Разработано с ❤️ для сообщества Telegram</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                <strong>Deployment:</strong> Vercel | 
                <strong>Framework:</strong> Flask | 
                <strong>Version:</strong> 2.0.0
            </p>
        </div>
    </div>
</body>
</html>
'''

# 🎨 КЛАВИАТУРЫ ДЛЯ ТЕЛЕГРАММ
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Функции", callback_data="features")],
        [InlineKeyboardButton("📊 Статус", callback_data="status")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton("💡 Помощь", callback_data="help")],
        [InlineKeyboardButton("🌐 Ссылки", callback_data="links")]
    ]
    return InlineKeyboardMarkup(keyboard)

def features_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Создать заметку", callback_data="create_note")],
        [InlineKeyboardButton("🎯 Задачи", callback_data="tasks")],
        [InlineKeyboardButton("📅 Календарь", callback_data="calendar")],
        [InlineKeyboardButton("📊 Аналитика", callback_data="analytics")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def links_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌐 Vercel Приложение", url=VERCEL_URL)],
        [InlineKeyboardButton("💻 GitHub Репозиторий", url=GITHUB_REPO)],
        [InlineKeyboardButton("📚 Документация", url="https://core.telegram.org/bots/api")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

# 🌐 FLASK ROUTES
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, 
        user_count=len(user_data),
        vercel_url=VERCEL_URL,
        github_repo=GITHUB_REPO
    )

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "fenix_ai",
        "version": "2.0.0",
        "users_count": len(user_data),
        "deployment": "vercel"
    })

@app.route('/api/status')
def api_status():
    return jsonify({
        "web_app": "running",
        "telegram_bot": "running", 
        "users_count": len(user_data),
        "deployment": "vercel",
        "url": VERCEL_URL
    })

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

# 💬 TELEGRAM HANDLERS (упрощенные)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    user_data[chat_id] = {
        "name": user.first_name,
        "username": user.username,
        "start_count": user_data.get(chat_id, {}).get("start_count", 0) + 1
    }
    
    await update.message.reply_text(
        f"✨ *Добро пожаловать, {user.first_name}!* ✨\n\n"
        f"🌐 *Веб-приложение:* {VERCEL_URL}\n"
        f"🚀 *Бот обновлен!* Новый дизайн!\n\n"
        f"Выбери действие:",
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "status":
        await query.edit_message_text(
            f"📊 *Статус системы*\n\n"
            f"*Веб-приложение:* ✅ Активно\n"
            f"*URL:* {VERCEL_URL}\n"
            f"*Пользователей:* {len(user_data)}\n"
            f"*Бот:* ✅ Работает\n\n"
            f"💡 Все системы в норме!",
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard()
        )
    elif query.data == "links":
        await query.edit_message_text(
            "🌐 *Полезные ссылки*\n\nБыстрый доступ:",
            parse_mode='Markdown',
            reply_markup=links_keyboard()
        )
    else:
        await query.edit_message_text(
            "🎮 *Главное меню*\n\nВыбери раздел:",
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard()
        )

# 🚀 НАСТРОЙКА ОБРАБОТЧИКОВ
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))

# Для Vercel
if __name__ == '__main__':
    app.run(debug=True)
