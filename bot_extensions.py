from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database_extensions import MovieDatabaseExtensions
from movie_utils import format_movie_list, format_movie_info

db_ext = MovieDatabaseExtensions()

async def extended_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ورژن توسعه یافته start با منوی ادمین پیشرفته"""
    user = update.effective_user
    db_ext.add_user(user.id, user.username, user.first_name, user.last_name)
    
    keyboard = [
        [InlineKeyboardButton("🎬 لیست فیلم‌ها", callback_data="show_movies")],
    ]
    
    if is_admin(user.id):
        # منوی ادمین پیشرفته
        keyboard.extend([
            [InlineKeyboardButton("➕ افزودن فیلم (ادمین)", callback_data="add_movie")],
            [InlineKeyboardButton("🛠️ مدیریت فیلم‌ها (ادمین)", callback_data="admin_manage_movies")]
        ])
    
    keyboard.append([InlineKeyboardButton("📞 پشتیبانی", url="https://t.me/your_channel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎭 به ربات فیلم خوش آمدید!\n"
        "روی دکمه زیر کلیک کن تا فیلم‌ها رو ببینی:",
        reply_markup=reply_markup
    )

async def extended_show_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ورژن توسعه یافته نمایش فیلم‌ها با تعداد دانلود"""
    query = update.callback_query
    await query.answer()
    
    movies = db_ext.get_all_movies()
    
    if not movies:
        await query.edit_message_text("📭 هیچ فیلمی در حال حاضر موجود نیست.")
        return
    
    # استفاده از فرمت‌بندی جدید
    text = format_movie_list(movies)
    
    keyboard = []
    for movie in movies:
        download_count = db_ext.get_movie_download_count(movie['id'])
        button_text = f"{movie['title']} ({download_count} 📥)"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"movie_{movie['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 برگشت", callback_data="back_to_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')

async def extended_send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ورژن توسعه یافته ارسال فیلم با شمارش دانلود"""
    query = update.callback_query
    await query.answer()
    
    movie_id = int(query.data.replace("movie_", ""))
    movie_data = db_ext.get_movie_by_id(movie_id)
    
    if not movie_data:
        await query.edit_message_text("❌ متاسفانه این فیلم در دسترس نیست.")
        return
    
    try:
        # افزایش تعداد دانلود
        db_ext.increment_download_count(movie_id)
        
        # نمایش اطلاعات فیلم با تعداد دانلود به روز شده
        current_downloads = db_ext.get_movie_download_count(movie_id)
        
        # ارسال فیلم
        message = await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=movie_data["file_id"],
            caption=f"🎬 {movie_data['title']}\n📥 تعداد دانلود: {current_downloads}"
        )
        
        # بقیه کد مانند قبل...
        warning_msg = await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚠️ این پست تا 30 ثانیه دیگر حذف خواهد شد..."
        )
        
        await asyncio.sleep(30)
        
        try:
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=message.message_id)
            await context.bot.delete_message(chat_id=query.message.chat_id, message_id=warning_msg.message_id)
        except:
            pass
            
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✅ فیلم با موفقیت ارسال شد!\nبرای دریافت فیلم‌های بیشتر روی /start کلیک کن."
        )
        
    except Exception as e:
        await query.edit_message_text("❌ خطا در ارسال فیلم. لطفا بعدا تلاش کن.")

# تابع کمکی برای بررسی ادمین (مثل قبل)
def is_admin(user_id):
    from bot import ADMIN_IDS  # ایمپورت از فایل اصلی
    return user_id in ADMIN_IDS