from flask import Flask, request
import telebot
from telebot import types
from waitress import serve

# === НАСТРОЙКИ ===
TOKEN = "7892998801:AAFxY1aSf-2npCc2d8g0f8VOt_ssWKBse8s"
AUTHORIZED_USERS = [760203245]  # пока только ты
WEBHOOK_URL = f"https://<render-url>.onrender.com/{TOKEN}"  # заменим позже

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === КНОПКИ ===
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ Доход", "➖ Расход")
    markup.add("📊 Статистика", "📋 История")
    markup.add("⚙️ Баланс")
    return markup

# === ДОСТУП ===
def is_authorized(message):
    return message.from_user.id in AUTHORIZED_USERS

# === СТАРТ ===
@bot.message_handler(commands=["start"])
def start(message):
    if not is_authorized(message):
        return bot.send_message(message.chat.id, "❌ Доступ запрещён.")
    bot.send_message(message.chat.id, "👋 Привет! Добро пожаловать в Финансового Бота!", reply_markup=main_menu())

@bot.message_handler(func=lambda m: is_authorized(m))
def handle_message(message):
    if message.text == "➕ Доход":
        bot.send_message(message.chat.id, "💰 Ввод дохода — скоро будет готово.")
    elif message.text == "➖ Расход":
        bot.send_message(message.chat.id, "🧾 Ввод расхода — скоро будет готово.")
    elif message.text == "📊 Статистика":
        bot.send_message(message.chat.id, "📈 Статистика — в разработке.")
    elif message.text == "📋 История":
        bot.send_message(message.chat.id, "🗂 История операций — в разработке.")
    elif message.text == "⚙️ Баланс":
        bot.send_message(message.chat.id, "💼 Баланс — будет позже.")
    else:
        bot.send_message(message.chat.id, "🚧 Функция пока недоступна.")

# === WEBHOOK ===
bot.remove_webhook()
import time; time.sleep(1)
bot.set_webhook(url=WEBHOOK_URL)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=10000)
