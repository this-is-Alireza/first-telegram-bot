import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from database import MovieDatabase

BOT_TOKEN = "8591604751:AAF2JtpBku6xigI63zrdIH-OahherAtPBXE"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

db = MovieDatabase()


ADMIN_IDS = [7642451106, 6783165751, 404156297]

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name, user.last_name)
    
    keyboard = [
        [InlineKeyboardButton("🎬 لیست فیلم‌ها", callback_data="show_movies")],
    ]
    
    if is_admin(user.id):
        keyboard.append([InlineKeyboardButton("➕ افزودن فیلم (ادمین)", callback_data="add_movie")])
    
    keyboard.append([InlineKeyboardButton("📞 پشتیبانی", url="https://t.me/your_channel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎭 به ربات فیلم خوش آمدید!\n"
        "روی دکمه زیر کلیک کن تا فیلم‌ها رو ببینی:",
        reply_markup=reply_markup
    )

async def show_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    movies = db.get_all_movies()
    
    if not movies:
        await query.edit_message_text("📭 هیچ فیلمی در حال حاضر موجود نیست.")
        return
    
    keyboard = []
    for movie in movies:
        keyboard.append([InlineKeyboardButton(movie["title"], callback_data=f"movie_{movie['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎥 لیست فیلم‌های موجود:\n"
        "روی فیلم مورد نظرت کلیک کن:",
        reply_markup=reply_markup
    )

async def add_movie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if not is_admin(query.from_user.id):
        await query.edit_message_text("❌ شما دسترسی ادمین ندارید!")
        return
    
    await query.edit_message_text(
        "📤 لطفاً فیلم رو ارسال کن و در کپشن آن:\n"
        "1. عنوان فیلم\n"
        "2. دسته‌بندی (اختیاری)\n\n"
        "مثال کپشن:\n"
        "«فیلم اکشن 2024»\n"
        "یا\n"
        "«فیلم کمدی|comedy»"
    )
    # حالت انتظار برای دریافت فیلم
    context.user_data['waiting_for_movie'] = True

async def receive_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return
    
    if update.message.video and context.user_data.get('waiting_for_movie'):
        video = update.message.video
        caption = update.message.caption or "فیلم بدون عنوان"
        
        # پردازش کپشن
        if "|" in caption:
            title, category = caption.split("|", 1)
            title = title.strip()
            category = category.strip()
        else:
            title = caption
            category = "general"
        
        # ذخیره فیلم در دیتابیس
        success = db.add_movie(title, video.file_id, caption, category)
        
        if success:
            await update.message.reply_text(
                f"✅ فیلم با موفقیت اضافه شد!\n"
                f"📝 عنوان: {title}\n"
                f"📁 دسته: {category}\n"
                f"🆔 File ID: {video.file_id[:20]}..."
            )
        else:
            await update.message.reply_text("❌ خطا در اضافه کردن فیلم. ممکن است عنوان تکراری باشد.")
        
        context.user_data['waiting_for_movie'] = False

async def send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    movie_id = int(query.data.replace("movie_", ""))
    movies = db.get_all_movies()
    movie_data = next((m for m in movies if m["id"] == movie_id), None)
    
    if not movie_data:
        await query.edit_message_text("❌ متاسفانه این فیلم در دسترس نیست.")
        return
    
    try:
        # ارسال فیلم
        message = await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=movie_data["file_id"],
            caption=movie_data["caption"] or "🎬 فیلم مورد نظر شما"
        )
        
        # پیام هشدار
        warning_msg = await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ این پست تا 30 ثانیه دیگر حذف خواهد شد..."
        )
        
        # انتظار 30 ثانیه
        await asyncio.sleep(30)
        
        # حذف فیلم و پیام
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=message.message_id)
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=warning_msg.message_id)
        except:
            pass
            
        # پیام نهایی
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✅ فیلم با موفقیت ارسال شد!\nبرای دریافت فیلم‌های بیشتر روی /start کلیک کن."
        )
        
    except Exception as e:
        await query.edit_message_text("❌ خطا در ارسال فیلم. لطفا بعدا تلاش کن.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "show_movies":
        await show_movies(update, context)
    elif data == "back_to_main":
        await start(update, context)
    elif data == "add_movie":
        await add_movie_handler(update, context)
    elif data.startswith("movie_"):
        await send_movie(update, context)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.VIDEO, receive_movie))
    
    print("🤖 Movie Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()

