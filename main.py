import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

API_URL = "https://imdb.iamidiotareyoutoo.com/?q="  # API مجانية بدون مفتاح

BOT_TOKEN = os.getenv("BOT_TOKEN")  # تأكد من ضبط متغير البيئة في Railway أو استخدم مباشرة التوكن

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 أرسل اسم أي فيلم أو مسلسل وسأجلب لك المعلومات عنه.")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("❗ يرجى كتابة اسم الفيلم أو المسلسل.")
        return

    url = API_URL + query
    response = requests.get(url)
    
    if response.status_code != 200:
        await update.message.reply_text("⚠️ حدث خطأ أثناء الاتصال بالمخدم.")
        return

    try:
        results = response.json().get("description", [])
        if not results:
            await update.message.reply_text("🙁 لم أجد نتائج.")
            return

        movie = results[0]
        title = movie.get("title", "بدون عنوان")
        image = movie.get("image", "")
        rating = movie.get("rating", "؟")
        url = movie.get("url", "")

        caption = f"*{title}*\n⭐ التقييم: {rating}\n🔗 [رابط IMDb]({url})"
        await update.message.reply_photo(photo=image, caption=caption, parse_mode="Markdown")
    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text("⚠️ حدث خطأ أثناء معالجة البيانات.")

def main():
    token = BOT_TOKEN or "ضع_رمز_البوت_هنا_إذا_لم_تستخدم_متغير_بيئة"

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
