from flask import Flask, request
import requests
import time

app = Flask(__name__)
TOKEN = '7308654023:AAF1hdW4f6VyeZnkn0kX946kIY6k7_xz9ZU'
URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(URL + "/getUpdates", params=params)
    result_json = response.json()['result']
    return result_json

def send_message(chat_id, text, reply_markup=None):
    params = {'chat_id': chat_id, 'text': text, 'reply_markup': reply_markup}
    response = requests.post(URL + "/sendMessage", json=params)
    return response

def handle_updates(updates):
    for update in updates:
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message']['text']
            if text == '/start':
                web_app_url = 'https://max2409.github.io/cliker.github.io/index.html'
                reply_markup = {
                    "inline_keyboard": [[
                        {
                            "text": "Open Mini App",
                            "web_app": {"url": web_app_url}
                        }
                    ]]
                }
                send_message(chat_id, 'Запустите веб-приложение!', reply_markup)

@app.route('/')
def index():
    return 'Bot is running'

if __name__ == '__main__':
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates:
            last_update_id = updates[-1]['update_id'] + 1
            handle_updates(updates)
        time.sleep(1)
    app.run(port=5000)
