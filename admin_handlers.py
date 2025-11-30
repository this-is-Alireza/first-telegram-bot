from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from database import MovieDatabase

db = MovieDatabase()

async def admin_manage_movies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت فیلم‌ها توسط ادمین"""
    query = update.callback_query
    await query.answer()
    
    movies = db.get_all_movies()
    
    if not movies:
        await query.edit_message_text("📭 هیچ فیلمی برای مدیریت وجود ندارد.")
        return
    
    text = "🎬 **مدیریت فیلم‌ها**\n\n"
    keyboard = []
    
    for movie in movies:
        # نمایش آمار دانلود هر فیلم
        download_count = db.get_movie_download_count(movie['id'])
        text += f"📹 {movie['title']}\n"
        text += f"   📥 دانلودها: {download_count}\n"
        text += f"   🆔 ID: {movie['id']}\n\n"
        
        # دکمه‌های مدیریت برای هر فیلم
        keyboard.append([
            InlineKeyboardButton(f"🗑️ حذف {movie['title'][:15]}...", callback_data=f"delete_movie_{movie['id']}")
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 برگشت به منوی اصلی", callback_data="back_to_main")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='HTML')

async def delete_movie_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تأیید حذف فیلم"""
    query = update.callback_query
    await query.answer()
    
    movie_id = int(query.data.replace("delete_movie_", ""))
    movie = db.get_movie_by_id(movie_id)
    
    if not movie:
        await query.edit_message_text("❌ فیلم مورد نظر یافت نشد.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ بله، حذف کن", callback_data=f"confirm_delete_{movie_id}"),
            InlineKeyboardButton("❌ خیر، برگرد", callback_data="admin_manage_movies")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"⚠️ **آیا مطمئن هستید می‌خواهید این فیلم را حذف کنید؟**\n\n"
        f"📹 عنوان: {movie['title']}\n"
        f"📁 دسته: {movie['category']}\n"
        f"📥 تعداد دانلود: {movie['download_count']}\n\n"
        f"❌ این عمل غیرقابل بازگشت است!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def confirm_delete_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """حذف نهایی فیلم"""
    query = update.callback_query
    await query.answer()
    
    movie_id = int(query.data.replace("confirm_delete_", ""))
    
    success = db.delete_movie(movie_id)
    
    if success:
        await query.edit_message_text("✅ فیلم با موفقیت حذف شد!")
        # بازگشت به منوی مدیریت
        await admin_manage_movies(update, context)
    else:
        await query.edit_message_text("❌ خطا در حذف فیلم. لطفاً دوباره تلاش کنید.")

def register_admin_handlers(application):
    """ثبت هندلرهای ادمین"""
    application.add_handler(CallbackQueryHandler(admin_manage_movies, pattern="^admin_manage_movies$"))
    application.add_handler(CallbackQueryHandler(delete_movie_confirmation, pattern="^delete_movie_"))
    application.add_handler(CallbackQueryHandler(confirm_delete_movie, pattern="^confirm_delete_"))