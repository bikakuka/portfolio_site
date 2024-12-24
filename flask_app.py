from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS
import hashlib
import hmac
import requests

app = Flask(__name__)
CORS(app)  # Включаем CORS

GITHUB_CLIENT_ID = 'Ov23liE2teDSY9aD4lJ1'
GITHUB_CLIENT_SECRET = 'f89fda40e53f1dd767949509f4bad94f48ddeaec'
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
GITHUB_USER_URL = 'https://api.github.com/user'

# Секретный ключ для сессии
app.secret_key = 'keykeykey1'  # Замените на свой секретный ключ

# Ваш секретный ключ бота (из BotFather)
BOT_TOKEN = "7618232417:AAGCfjmk7v-og9BOUfJeTBk7Z9Y-PDPKmmE"

@app.route('/')
def home():
    user = session.get('user')
    print("Session data in /:", user)  # Отладочный вывод
    return render_template('Page-2.html', user=user)

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'GET':
        # Обработка GET-запроса (Telegram)
        data = request.args.to_dict()

        # Проверка подписи
        hash = data.pop('hash')
        check_hash = hmac.new(
            key=BOT_TOKEN.encode(),
            msg='\n'.join(f'{k}={v}' for k, v in sorted(data.items())).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        #if check_hash != hash:
         #   return jsonify({'error': 'Invalid hash'}), 400

        # Сохраняем данные пользователя в сессии
        session['user'] = {
            'id': data.get('id'),
            'username': data.get('username'),
            'name': f"{data.get('first_name')} {data.get('last_name')}",
            'avatar_url': data.get('photo_url'),
            'source': 'telegram'  # Источник авторизации
        }

        return redirect(url_for('home'))

    elif request.method == 'POST':
        # Обработка POST-запроса (Telegram)
        data = request.form.to_dict()

        # Проверка подписи
        hash = data.pop('hash')
        check_hash = hmac.new(
            key=BOT_TOKEN.encode(),
            msg='\n'.join(f'{k}={v}' for k, v in sorted(data.items())).encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        #if check_hash != hash:
        #    return jsonify({'error': 'Invalid hash'}), 400

        # Сохраняем данные пользователя в сессии
        session['user'] = {
            'id': data.get('id'),
            'username': data.get('username'),
            'name': f"{data.get('first_name')} {data.get('last_name')}",
            'avatar_url': data.get('photo_url'),
            'source': 'telegram'  # Источник авторизации
        }

        return redirect(url_for('home'))

@app.route('/login/github')
def login_github():
    # Перенаправляем пользователя на страницу авторизации GitHub
    return redirect(f'{GITHUB_AUTHORIZE_URL}?client_id={GITHUB_CLIENT_ID}&scope=user')

@app.route('/github/callback')
def github_callback():
    # Получаем код из параметров запроса
    code = request.args.get('code')

    # Обмениваем код на токен доступа
    token_response = requests.post(GITHUB_TOKEN_URL, data={
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code
    }, headers={'Accept': 'application/json'})

    access_token = token_response.json().get('access_token')

    if not access_token:
        return 'Failed to get access token', 400

    # Получаем данные пользователя с помощью токена доступа
    user_response = requests.get(GITHUB_USER_URL, headers={
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    })

    user_data = user_response.json()

    # Сохраняем данные пользователя в сессии
    session['user'] = {
        'id': user_data.get('id'),
        'username': user_data.get('login'),
        'name': user_data.get('name'),
        'avatar_url': user_data.get('avatar_url'),
        'source': 'github'  # Источник авторизации
    }

    # Перенаправляем на главную страницу
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    # Удаляем данные пользователя из сессии
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route("/yandex_4a18081ed921666f.html")
def webmaster():
    return render_template("yandex_4a18081ed921666f.html")

if __name__ == '__main__':
    app.run(debug=True)