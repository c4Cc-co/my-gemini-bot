import os
import telebot
import google.generativeai as genai

# جلب المفاتيح من إعدادات الاستضافة
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# إعداد جيمناي بنسخة فلاش المستقرة
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم التحديث! أنا الآن جاهز للرد.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"خطأ في المفتاح أو الخدمة: {str(e)}")

bot.infinity_polling()
