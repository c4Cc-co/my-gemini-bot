import os
import telebot
import google.generativeai as genai

# جلب الإعدادات
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# إعداد جيمناي
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت ذكاء اصطناعي، اسألني أي شيء بالعربي.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # إجبار النموذج على الرد بالعربية عبر البرومبت
        response = model.generate_content(f"Answer in Arabic: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "حدث خطأ، حاول مرة أخرى.")

# تشغيل نهائي ومستقر
bot.infinity_polling(timeout=90, long_polling_timeout=90)
