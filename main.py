
import os
import threading
import time
import requests
from flask import Flask, request

# Настройки
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL")
KEYWORDS = [
    "мигрант", "миграция", "трудовой", "патент", "внж", "рвп", "гражданство",
    "экзамен", "русский язык", "тестирование", "депортация", "штраф", "регистрация",
    "работодатель", "индия", "узбекистан", "таджикистан", "киргизия", "вьетнам"
]

SOURCE_URLS = [
    "https://www.gazeta.ru",
    "https://www.kommersant.ru"
]

# Функция парсинга (заглушка — сюда вставим парсинг позже)
def check_sources():
    print("Парсер работает...")
    for url in SOURCE_URLS:
        try:
            r = requests.get(url, timeout=10)
            if any(kw in r.text.lower() for kw in KEYWORDS):
                send_message(f"Обнаружено упоминание ключевых слов на {url}")
        except Exception as e:
            print(f"Ошибка при проверке {url}: {e}")
    print("Парсинг завершён")

# Отправка сообщения в Telegram
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text[:4096], "disable_web_page_preview": True}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

# Поток для постоянной работы
def start_worker():
    while True:
        check_sources()
        time.sleep(600)  # каждые 10 минут

# Flask веб-сервер
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает."

# Стартуем фоновый поток и сервер
if __name__ == "__main__":
    threading.Thread(target=start_worker, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)
