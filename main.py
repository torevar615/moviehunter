import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
import requests

# سجل الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# استبدل التوكن بتوكن بوتك
TELEGRAM_BOT_TOKEN = "7644193561:AAEH_CsjSZoyiG3bMLmHDZsnLkUKbg6Wk1k"

# مفتاح API الخاص بـ TMDb
TMDB_API_KEY = "fcbe1d791fe9eafa50c3107c011ff73a"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# بحث عن الأفلام في TMDb
def search_movie(query):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1,
        'include_adult': False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا! أرسل لي اسم أي فيلم وسأبحث لك عنه."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أرسل اسم فيلم للبحث عنه.\n"
        "سأرسل لك معلومات عنه وروابط تحميل (إذا كانت متوفرة)."
    )

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    if not query:
        await update.message.reply_text("من فضلك أرسل اسم فيلم صحيح.")
        return
    
    await update.message.chat.send_action(action="typing")

    data = search_movie(query)
    if not data or data['total_results'] == 0:
        await update.message.reply_text("عذرًا، لم أجد أي نتائج لهذا الفيلم.")
        return
    
    results = data['results'][:5]  # اعرض أول 5 نتائج فقط
    
    for movie in results:
        title = movie.get('title', 'N/A')
        release_date = movie.get('release_date', 'N/A')
        overview = movie.get('overview', 'لا توجد معلومات')
        movie_id = movie.get('id')
        poster_path = movie.get('poster_path')

        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        text = f"*{title}* ({release_date})\n\n{overview}"

        # أزرار روابط (زر التفاصيل في TMDb وزر وهمي تحميل)
        keyboard = [
            [
                InlineKeyboardButton("تفاصيل أكثر", url=f"https://www.themoviedb.org/movie/{movie_id}"),
                InlineKeyboardButton("تحميل", callback_data=f"download_{movie_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if poster_url:
            await update.message.reply_photo(photo=poster_url, caption=text, parse_mode="Markdown", reply_markup=reply_markup)
        else:
            await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("download_"):
        movie_id = data.split("_")[1]
        # هنا يمكنك إضافة رابط تحميل فعلي إذا وجد
        # TMDb لا يوفر روابط تحميل، لذا نرسل رسالة وهمية أو توجه المستخدم لمصادر أخرى
        await query.edit_message_caption(caption="عذرًا، روابط التحميل غير متوفرة في الوقت الحالي.\nيمكنك البحث عن الفيلم في مواقع التحميل الموثوقة.")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_search))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("البوت يعمل الآن ...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
