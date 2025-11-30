from database import MovieDatabase

db = MovieDatabase()

def format_movie_list(movies):
    """فرمت‌بندی لیست فیلم‌ها با نمایش تعداد دانلود"""
    if not movies:
        return "📭 هیچ فیلمی موجود نیست."
    
    text = "🎥 **لیست فیلم‌های موجود:**\n\n"
    
    for movie in movies:
        download_count = db.get_movie_download_count(movie['id'])
        text += f"📹 {movie['title']}\n"
        text += f"   📥 تعداد دانلود: {download_count}\n"
        text += f"   📁 دسته: {movie['category']}\n\n"
    
    return text

def format_movie_info(movie):
    """فرمت‌بندی اطلاعات یک فیلم"""
    download_count = db.get_movie_download_count(movie['id'])
    
    text = (
        f"🎬 **{movie['title']}**\n"
        f"📁 دسته‌بندی: {movie['category']}\n"
        f"📥 تعداد دانلود: {download_count}\n"
        f"📝 توضیحات: {movie['caption'] or 'بدون توضیح'}\n\n"
        f"⬇️ برای دانلود فیلم، روی دکمه زیر کلیک کن:"
    )
    
    return text