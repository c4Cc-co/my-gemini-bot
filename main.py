import os
import telebot
import google.generativeai as genai

# جلب المفاتيح من إعدادات الاستضافة
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# إعداد جيمناي بنسخة فلاش المستقرة
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "تم التحديث بنجاح! أنا الآن جاهز للرد على استفساراتك.")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # إرسال النص لجيمناي والحصول على الرد
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "اعتذر، لم أستطع تكوين رد حالياً.")
    except Exception as e:
        # إرسال رسالة توضح نوع الخطأ إذا حدث
        bot.reply_to(message, f"حدث خطأ في الاتصال بجيمناي: {str(e)}")

# تشغيل البوت بشكل مستمر
bot.infinity_polling()
