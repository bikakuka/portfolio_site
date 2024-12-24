from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)

# Ваш секретный ключ бота (из BotFather)
BOT_TOKEN = "7618232417:AAGCfjmk7v-og9BOUfJeTBk7Z9Y-PDPKmmE"

@app.route('/auth', methods=['POST'])
def auth():
    data = request.form.to_dict()

    # Проверка подписи
    hash = data.pop('hash')
    check_hash = hmac.new(
        key=BOT_TOKEN.encode(),
        msg='\n'.join(f'{k}={v}' for k, v in sorted(data.items())).encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if check_hash != hash:
        return jsonify({'error': 'Invalid hash'}), 400

    # Данные корректны, авторизуем пользователя
    user_id = data.get('id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    photo_url = data.get('photo_url')

    # Здесь вы можете сохранить данные пользователя в базу данных или сессию
    return jsonify({
        'message': 'Authorization successful',
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'photo_url': photo_url
    }), 200

if __name__ == '__main__':
    app.run(debug=True)