import os
import telebot
import google.generativeai as genai

# جلب المفاتيح من إعدادات الاستضافة
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# إعداد ذكاء Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت ذكاء اصطناعي. اسألني أي شيء.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "حدث خطأ في معالجة الطلب.")

bot.infinity_polling()
