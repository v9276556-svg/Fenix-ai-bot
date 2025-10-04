from flask import Flask, request, jsonify, render_template_string
import requests
import json

app = Flask(__name__)

VERCEL_API_URL = "https://fenix-ai-bot-tau.vercel.app"

# Telegram Web App HTML с JavaScript для работы с API
TELEGRAM_WEBAPP_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fenix AI - Web App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 100%;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            padding: 30px 20px;
        }
        
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 24px;
            font-weight: 600;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .btn {
            display: block;
            width: 100%;
            padding: 15px;
            background: #0088cc;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 500;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            background: #0077b3;
            transform: translateY(-1px);
        }
        
        .btn-secondary {
            background: #6c757d;
        }
        
        .feature {
            padding: 15px;
            border-left: 4px solid #0088cc;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .status {
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: center;
            font-weight: 500;
        }
        
        .status.healthy {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .user-info {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border: 1px solid #b3d9ff;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Fenix AI</h1>
            <p>Web App внутри Telegram • Vercel API</p>
        </div>
        
        <div id="userInfo" class="user-info hidden">
            <strong>👤 Информация о пользователе</strong>
            <div id="userData">Загрузка...</div>
        </div>
        
        <div class="card">
            <h3>🚀 Быстрые действия</h3>
            <button class="btn" onclick="checkHealth()">📊 Проверить статус API</button>
            <button class="btn" onclick="getBotInfo()">🤖 Информация о боте</button>
            <button class="btn btn-secondary" onclick="sendToBot('help')">💡 Получить помощь</button>
        </div>
        
        <div id="statusCard" class="card hidden">
            <h3>📈 Статус системы</h3>
            <div id="statusContent"></div>
        </div>
        
        <div class="card">
            <h3>🌐 Интеграции</h3>
            <div class="feature">
                <strong>Vercel API</strong>
                <p>Сервер развернут на Vercel</p>
                <small id="apiStatus">Проверка соединения...</small>
            </div>
            <div class="feature">
                <strong>Telegram Bot</strong>
                <p>Полная интеграция с ботом</p>
            </div>
            <div class="feature">
                <strong>Web App</strong>
                <p>Работает внутри Telegram</p>
            </div>
        </div>
        
        <div class="card">
            <h3>⚡ Тестирование API</h3>
            <button class="btn" onclick="testEndpoint('/health')">Тест /health</button>
            <button class="btn" onclick="testEndpoint('/api/status')">Тест /api/status</button>
            <button class="btn btn-secondary" onclick="showUserData()">Показать данные Telegram</button>
        </div>
    </div>

    <script>
        // Инициализация Telegram Web App
        let tg = window.Telegram.WebApp;
        
        // Показываем главную кнопку
        tg.MainButton.setText("ЗАКРЫТЬ WEB APP").show().onClick(function() {
            tg.close();
        });
        
        // Расширяем на весь экран
        tg.expand();
        
        // Показываем данные пользователя
        function showUserData() {
            const user = tg.initDataUnsafe.user;
            const userInfo = document.getElementById('userInfo');
            const userData = document.getElementById('userData');
            
            if (user) {
                userData.innerHTML = `
                    <div>ID: ${user.id}</div>
                    <div>Имя: ${user.first_name}</div>
                    <div>Фамилия: ${user.last_name || 'Не указана'}</div>
                    <div>Username: @${user.username || 'Не указан'}</div>
                    <div>Язык: ${user.language_code || 'Не указан'}</div>
                `;
                userInfo.classList.remove('hidden');
            } else {
                userData.innerHTML = 'Данные пользователя недоступны';
                userInfo.classList.remove('hidden');
            }
        }
        
        // Проверка здоровья API
        async function checkHealth() {
            showLoading('statusContent', 'Проверка API...');
            document.getElementById('statusCard').classList.remove('hidden');
            
            try {
                const response = await fetch('{{ vercel_url }}/health');
                const data = await response.json();
                
                document.getElementById('statusContent').innerHTML = `
                    <div class="status healthy">
                        ✅ API работает нормально
                    </div>
                    <div><strong>Сервис:</strong> ${data.service}</div>
                    <div><strong>Версия:</strong> ${data.version}</div>
                    <div><strong>Статус:</strong> ${data.status}</div>
                    <div><strong>Время:</strong> ${new Date().toLocaleTimeString()}</div>
                `;
                
                // Обновляем статус в features
                document.getElementById('apiStatus').innerHTML = '✅ Соединение установлено';
                document.getElementById('apiStatus').style.color = 'green';
                
            } catch (error) {
                document.getElementById('statusContent').innerHTML = `
                    <div class="status error">
                        ❌ Ошибка подключения к API
                    </div>
                    <div>${error.message}</div>
                `;
                
                document.getElementById('apiStatus').innerHTML = '❌ Ошибка соединения';
                document.getElementById('apiStatus').style.color = 'red';
            }
        }
        
        // Получение информации о боте
        async function getBotInfo() {
            showLoading('statusContent', 'Получение информации о боте...');
            document.getElementById('statusCard').classList.remove('hidden');
            
            try {
                const response = await fetch('{{ vercel_url }}/api/status');
                const data = await response.json();
                
                document.getElementById('statusContent').innerHTML = `
                    <div class="status healthy">
                        🤖 Бот активен
                    </div>
                    <div><strong>Web App:</strong> ${data.web_app}</div>
                    <div><strong>Telegram Bot:</strong> ${data.telegram_bot}</div>
                    <div><strong>Пользователей:</strong> ${data.users_count}</div>
                    <div><strong>Деплой:</strong> ${data.deployment}</div>
                    <div><strong>URL:</strong> ${data.url}</div>
                `;
            } catch (error) {
                document.getElementById('statusContent').innerHTML = `
                    <div class="status error">
                        ❌ Ошибка получения данных
                    </div>
                    <div>${error.message}</div>
                `;
            }
        }
        
        // Тестирование endpoint
        async function testEndpoint(endpoint) {
            showLoading('statusContent', `Тестирование ${endpoint}...`);
            document.getElementById('statusCard').classList.remove('hidden');
            
            try {
                const response = await fetch(`{{ vercel_url }}${endpoint}`);
                const data = await response.json();
                
                document.getElementById('statusContent').innerHTML = `
                    <div class="status healthy">
                        ✅ ${endpoint} работает
                    </div>
                    <pre style="background: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto;">${JSON.stringify(data, null, 2)}</pre>
                `;
            } catch (error) {
                document.getElementById('statusContent').innerHTML = `
                    <div class="status error">
                        ❌ Ошибка ${endpoint}
                    </div>
                    <div>${error.message}</div>
                `;
            }
        }
        
        // Отправка данных боту
        function sendToBot(action) {
            const user = tg.initDataUnsafe.user;
            tg.sendData(JSON.stringify({
                action: action,
                user_id: user ? user.id : 'unknown',
                timestamp: new Date().getTime()
            }));
            
            // Показываем уведомление
            showNotification(`Команда "${action}" отправлена боту`);
        }
        
        // Вспомогательные функции
        function showLoading(elementId, text) {
            document.getElementById(elementId).innerHTML = `
                <div class="loading">
                    <div>${text}</div>
                    <div>⏳ Загрузка...</div>
                </div>
            `;
        }
        
        function showNotification(message) {
            tg.showPopup({
                title: "Уведомление",
                message: message,
                buttons: [{ type: "ok" }]
            });
        }
        
        // Автоматическая проверка при загрузке
        document.addEventListener('DOMContentLoaded', function() {
            showUserData();
            checkHealth();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Главная страница - Telegram Web App"""
    user_agent = request.headers.get('User-Agent', '').lower()
    
    # Если открыто в Telegram, показываем Web App
    if 'telegram' in user_agent:
        return render_template_string(TELEGRAM_WEBAPP_HTML, vercel_url=VERCEL_API_URL)
    else:
        # Для обычных браузеров
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Fenix AI - Web App</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 40px; 
                    text-align: center; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    min-height: 100vh;
                }
                .info { 
                    background: rgba(255,255,255,0.1); 
                    padding: 30px; 
                    border-radius: 15px; 
                    margin: 20px auto;
                    max-width: 500px;
                    backdrop-filter: blur(10px);
                }
            </style>
        </head>
        <body>
            <h1>🤖 Fenix AI Web App</h1>
            <div class="info">
                <h3>🚀 Специальное приложение для Telegram</h3>
                <p>Этот интерфейс предназначен для работы внутри Telegram Web App</p>
                <p><strong>Чтобы использовать:</strong></p>
                <p>1. Откройте бота в Telegram</p>
                <p>2. Нажмите кнопку "Открыть"</p>
                <p>3. Используйте интерактивный интерфейс</p>
                <p><strong>Бот:</strong> @fenix_ai_test_bot</p>
            </div>
        </body>
        </html>
        '''

@app.route('/health')
def health():
    """Health check для API"""
    return jsonify({
        "status": "healthy",
        "service": "fenix_ai_webapp",
        "version": "2.0.0",
        "timestamp": "2024-01-01T00:00:00Z",
        "environment": "vercel"
    })

@app.route('/api/status')
def api_status():
    """Статус системы"""
    return jsonify({
        "web_app": "running",
        "telegram_bot": "active",
        "users_count": 1,
        "deployment": "vercel",
        "url": VERCEL_API_URL
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для бота"""
    return jsonify({"status": "ok", "webapp": "connected"})

if __name__ == '__main__':
    app.run(debug=True)
