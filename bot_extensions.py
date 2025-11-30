async def extended_send_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ورژن توسعه یافته ارسال فیلم با شمارش دانلود - بدون حذف خودکار"""
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
        
        # ارسال فیلم (بدون حذف خودکار)
        await context.bot.send_video(
            chat_id=query.message.chat_id,
            video=movie_data["file_id"],
            caption=f"🎬 {movie_data['title']}\n📥 تعداد دانلود: {current_downloads}\n📝 {movie_data['caption'] or ''}"
        )
        
        # پیام تأیید
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✅ فیلم با موفقیت ارسال شد!\nبرای دریافت فیلم‌های بیشتر روی /start کلیک کن."
        )
        
    except Exception as e:
        await query.edit_message_text("❌ خطا در ارسال فیلم. لطفا بعدا تلاش کن.")
