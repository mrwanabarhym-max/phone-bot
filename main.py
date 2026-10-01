import os
import threading
from flask import Flask
import telebot
from telebot import types
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

API_TOKEN = "7828067814:AAHk3fT8YyUjUa9j8S5-yQzI_lW8-2A-3b4"
bot = telebot.TeleBot(API_TOKEN)

try:
    bot.remove_webhook()
except Exception:
    pass

BRANDING = "مِـآرَوُ ءلَ خــمورجـي //1> 𓅆"
CHANNEL_URL = "https://t.me/MAROO_32"

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton("قناة السورس ⚡", url=CHANNEL_URL)
    markup.add(channel_button)
    
    welcome_text = (
        f"أهلاً بك في بوت كشف معلومات الأرقام 📱\n"
        f"بواسطة: {BRANDING}\n\n"
        f"أرسل لي أي رقم هاتف بالصيغة الدولية لجلب بياناته.\n"
        f"مثال: `+201012345678`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def infonumber(message):
    user_input = message.text.strip().replace(" ", "")
    if not user_input.startswith("+"):
        user_input = "+" + user_input

    try:
        parsed_number = phonenumbers.parse(user_input, None)
        
        if not phonenumbers.is_valid_number(parsed_number):
            bot.reply_to(message, "❌ الرقم المدخل غير صحيح أو غير مستعمل.")
            return

        country = geocoder.description_for_number(parsed_number, "ar") or "غير معروف"
        service_provider = carrier.name_for_number(parsed_number, "ar") or "غير معروف"
        tz_list = timezone.time_zones_for_number(parsed_number)
        time_zone = ", ".join(tz_list) if tz_list else "غير معروف"
        
        int_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        num_type = phonenumbers.number_type(parsed_number)
        type_str = "محمول (Mobile)" if num_type == phonenumbers.PhoneNumberType.MOBILE else "خط أرضي / آخر"

        response_text = (
            f"🔍 **بيانات الرقم:**\n\n"
            f"📍 **الدولة / المنطقة:** {country}\n"
            f"📡 **المشغل / الشريحة:** {service_provider}\n"
            f"⏰ **التوقيت الزمني:** {time_zone}\n"
            f"📱 **نوع الخط:** {type_str}\n"
            f"🌐 **الصيغة الدولية:** `{int_format}`\n\n"
            f"حقوق: {BRANDING}"
        )

        markup = types.InlineKeyboardMarkup()
        wa_number = e164_format.replace("+", "")
        whatsapp_button = types.InlineKeyboardButton("مراسلة عبر واتساب 💬", url=f"https://wa.me/{wa_number}")
        markup.add(whatsapp_button)

        bot.reply_to(message, response_text, parse_mode="Markdown", reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, "❌ حدث خطأ أثناء تحليل الرقم. التأكد من كتابة كود الدولة بشكل صحيح.")

if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
