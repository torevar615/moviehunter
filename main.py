from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

API_URL = "https://search.imdbot.workers.dev/?q="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل اسم فيلم أو مسلسل للبحث عنه 🎬")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    res = requests.get(API_URL + query)
    data = res.json()
    
    if data.get("description"):
        first = data["description"][0]
        title = first.get("title", "بدون عنوان")
        image = first.get("image", "")
        rating = first.get("rating", "؟")
        link = first.get("url", "")
        
        caption = f"🎬 *{title}*\n⭐ التقييم: {rating}\n🔗 [رابط IMDb]({link})"
        await update.message.reply_photo(photo=image, caption=caption, parse_mode="Markdown")
    else:
        await update.message.reply_text("لم يتم العثور على نتائج.")

def main():
    TOKEN = "7644193561:AAEH_CsjSZoyiG3bMLmHDZsnLkUKbg6Wk1k"
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    
    app.run_polling()

if __name__ == "__main__":
    main()
