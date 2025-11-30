import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ایمپورت از فایل اصلی
from bot import BOT_TOKEN, db

# ایمپورت افزونه‌های جدید
from admin_handlers import register_admin_handlers
from bot_extensions import extended_start, extended_show_movies, extended_send_movie

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """هندلر اصلی برای دکمه‌ها"""
    query = update.callback_query
    data = query.data
    
    if data == "show_movies":
        await extended_show_movies(update, context)
    elif data == "back_to_main":
        await extended_start(update, context)
    elif data == "add_movie":
        from bot import add_movie_handler  # ایمپورت از فایل اصلی
        await add_movie_handler(update, context)
    elif data.startswith("movie_"):
        await extended_send_movie(update, context)
    else:
        # هندلرهای دیگر توسط admin_handlers مدیریت می‌شوند
        await query.answer()

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # استفاده از ورژن توسعه یافته start
    application.add_handler(CommandHandler("start", extended_start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # هندلرهای اصلی (بدون تغییر)
    from bot import receive_movie
    application.add_handler(MessageHandler(filters.VIDEO, receive_movie))
    
    # ثبت هندلرهای ادمین جدید
    register_admin_handlers(application)
    
    print("🤖 Movie Bot (Extended) is running...")
    application.run_polling()

if __name__ == "__main__":
    main()