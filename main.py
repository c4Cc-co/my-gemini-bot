import os
import telebot
import google.generativeai as genai

# إعداد المفاتيح من البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

# إعداد جيمناي - تم التغيير لضمان التوافق مع المكتبة
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت ذكاء اصطناعي مدعوم من جيمناي، كيف يمكنني مساعدتك اليوم؟")

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # توليد الرد من الذكاء الاصطناعي
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أستطع صياغة رد مناسب حالياً.")
            
    except Exception as e:
        # إرسال رسالة خطأ بسيطة للمستخدم
        bot.reply_to(message, "حدث خطأ بسيط في معالجة طلبك، يرجى المحاولة مرة أخرى.")
        print(f"Error: {e}")

# تشغيل البوت مع ضبط وقت الانتظار لتجنب الـ Timeout
bot.infinity_polling(timeout=60, long_polling_timeout=60)
