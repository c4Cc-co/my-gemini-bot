import os
import telebot
import google.generativeai as genai

# Setup Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# Configure Gemini with the correct model name
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I am now ready to chat.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "I couldn't generate a response.")
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Please try again, the service is busy.")

# Standard polling to avoid conflicts
bot.infinity_polling(timeout=90, long_polling_timeout=90)
