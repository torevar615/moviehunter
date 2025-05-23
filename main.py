import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

OMDB_API_KEY = "5c5df644"  # ضع مفتاحك هنا
BOT_TOKEN = os.getenv("BOT_TOKEN") or "ضع_توكن_البوت_هنا"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 أرسل اسم فيلم أو مسلسل باللغة الإنجليزية، وسأبحث لك عنه."
    )

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("❗ يرجى كتابة اسم الفيلم أو المسلسل.")
        return

    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={query}"
    response = requests.get(url)
    if response.status_code != 200:
        await update.message.reply_text("⚠️ حدث خطأ في الاتصال بالمخدم.")
        return

    data = response.json()
    if data.get("Response") == "False":
        await update.message.reply_text(f"🙁 لم أجد نتائج لـ '{query}'.")
        return

    title = data.get("Title", "لا يوجد عنوان")
    year = data.get("Year", "؟")
    rated = data.get("Rated", "؟")
    released = data.get("Released", "؟")
    runtime = data.get("Runtime", "؟")
    genre = data.get("Genre", "؟")
    director = data.get("Director", "؟")
    actors = data.get("Actors", "؟")
    plot = data.get("Plot", "لا يوجد ملخص")
    rating = data.get("imdbRating", "؟")
    poster = data.get("Poster", None)
    imdb_id = data.get("imdbID", "")

    caption = f"*{title}* ({year})\n"
    caption += f"⭐ تقييم IMDb: {rating}\n"
    caption += f"🎬 النوع: {genre}\n"
    caption += f"🕒 المدة: {runtime}\n"
    caption += f"👨‍🎨 المخرج: {director}\n"
    caption += f"🎭 الممثلون: {actors}\n\n"
    caption += f"📖 القصة:\n{plot}\n"
    caption += f"\n[رابط IMDb](https://www.imdb.com/title/{imdb_id}/)"

    keyboard = [
        [InlineKeyboardButton("🔗 رابط IMDb", url=f"https://www.imdb.com/title/{imdb_id}/")],
        [InlineKeyboardButton("⬇️ تحميل الفيلم", callback_data=f"download_{imdb_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if poster and poster != "N/A":
        await update.message.reply_photo(photo=poster, caption=caption, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await update.message.reply_text(caption, parse_mode="Markdown", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("download_"):
        imdb_id = data[len("download_"):]
        # هنا تضيف منطق تحميل الفيلم أو رابط تحميل حقيقي إذا توفر
        await query.message.reply_text(f"🔽 رابط تحميل الفيلم {imdb_id} سيضاف لاحقًا.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
