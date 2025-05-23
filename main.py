import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7644193561:AAEH_CsjSZoyiG3bMLmHDZsnLkUKbg6Wk1k"
OMDB_API_KEY = "b0465c6f"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أرسل اسم فيلم للبحث عنه.")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={query}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        await update.message.reply_text("⚠️ حدث خطأ في الاتصال بالمخدم.")
        return
    
    data = response.json()
    
    if data.get("Response") == "False":
        await update.message.reply_text(f"لم يتم العثور على فيلم باسم: {query}")
        return
    
    title = data.get("Title", "غير معروف")
    year = data.get("Year", "غير معروف")
    rated = data.get("Rated", "غير معروف")
    released = data.get("Released", "غير معروف")
    runtime = data.get("Runtime", "غير معروف")
    genre = data.get("Genre", "غير معروف")
    director = data.get("Director", "غير معروف")
    plot = data.get("Plot", "غير متوفر")
    imdb_rating = data.get("imdbRating", "غير معروف")
    poster = data.get("Poster")
    imdb_id = data.get("imdbID")
    
    msg = (f"🎬 *{title}* ({year})\n"
           f"⭐ تقييم IMDb: {imdb_rating}\n"
           f"📅 إصدار: {released}\n"
           f"⏳ المدة: {runtime}\n"
           f"🎭 النوع: {genre}\n"
           f"🎬 المخرج: {director}\n\n"
           f"📖 القصة:\n{plot}")
    
    buttons = []
    if imdb_id:
        imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
        buttons.append([InlineKeyboardButton("مشاهدة على IMDb", url=imdb_url)])
        # هنا يمكنك إضافة زر تحميل إذا كان لديك رابط تحميل حقيقي
        # buttons.append([InlineKeyboardButton("تحميل الفيلم", url="رابط_التحميل")])
    
    keyboard = InlineKeyboardMarkup(buttons) if buttons else None
    
    if poster and poster != "N/A":
        await update.message.reply_photo(photo=poster, caption=msg, parse_mode='Markdown', reply_markup=keyboard)
    else:
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=keyboard)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.run_polling()

if __name__ == "__main__":
    main()
