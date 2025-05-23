import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import aiohttp

# ضع هنا توكن بوت تيليجرام
BOT_TOKEN = "7644193561:AAEH_CsjSZoyiG3bMLmHDZsnLkUKbg6Wk1k"

# توكن TMDB API (مفتاح القراءة)
TMDB_API_TOKEN = "fcbe1d791fe9eafa50c3107c011ff73a"

# إعدادات اللوق
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أرسل لي /movie ثم اسم الفيلم للحصول على معلومات.")

async def get_movie_info(title: str):
    url = f"https://api.themoviedb.org/3/search/movie"
    headers = {
        "Authorization": f"Bearer {TMDB_API_TOKEN}",
        "Content-Type": "application/json;charset=utf-8"
    }
    params = {"query": title}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if data["results"]:
                movie = data["results"][0]
                return movie
            else:
                return None

async def movie_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("يرجى إرسال اسم الفيلم بعد الأمر /movie")
        return

    movie_name = " ".join(context.args)
    await update.message.reply_text(f"جاري البحث عن: {movie_name} ...")

    movie = await get_movie_info(movie_name)
    if movie:
        title = movie.get("title", "غير معروف")
        overview = movie.get("overview", "لا يوجد وصف")
        release_date = movie.get("release_date", "غير معروف")
        vote_average = movie.get("vote_average", "N/A")
        reply = (
            f"🎬 *{title}*\n"
            f"📅 تاريخ الإصدار: {release_date}\n"
            f"⭐ تقييم: {vote_average}\n"
            f"📖 نبذة:\n{overview}"
        )
        await update.message.reply_markdown(reply)
    else:
        await update.message.reply_text("لم أتمكن من العثور على الفيلم المطلوب.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("movie", movie_command))

    app.run_polling()

if __name__ == "__main__":
    main()
