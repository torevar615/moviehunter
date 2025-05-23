import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

API_URL = "https://imdb.iamidiotareyoutoo.com/?q="

BOT_TOKEN = os.getenv("BOT_TOKEN")  # أو ضع التوكن مباشرة هنا


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 أرسل اسم أي فيلم أو مسلسل باللغة الإنجليزية وسأجلب لك المعلومات عنه."
    )


async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("❗ يرجى كتابة اسم الفيلم أو المسلسل.")
        return

    url_api = API_URL + query
    response = requests.get(url_api)

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
        url_imdb = movie.get("url", "")

        caption = f"*{title}*\n⭐ التقييم: {rating}\n"

        keyboard = [
            [InlineKeyboardButton("🔗 رابط IMDb", url=url_imdb)],
            [InlineKeyboardButton("⬇️ تحميل الفيلم", callback_data=f"download_{title}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_photo(
            photo=image, caption=caption, parse_mode="Markdown", reply_markup=reply_markup
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text("⚠️ حدث خطأ أثناء معالجة البيانات.")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("download_"):
        movie_title = data[len("download_"):]
        # هنا تضيف رابط التحميل أو أي وظيفة تريدها
        await query.message.reply_text(f"🔽 رابط تحميل {movie_title} سيتم إضافته لاحقاً.")


def main():
    token = BOT_TOKEN or "ضع_توكن_البوت_هنا"

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
