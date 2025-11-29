from database import MovieDatabase

db = MovieDatabase()

# اضافه کردن فیلم‌ها
movies = [
    {
        "title": "فیلم اکشن 2024",
        "file_id": "BAACAgQAAxkBAAIB...",  # اینجا file_id واقعی رو بذار
        "caption": "🎬 فیلم اکشن جذاب 2024",
        "category": "action"
    },
    {
        "title": "فیلم کمدی", 
        "file_id": "BAACAgQAAxkBAAIB...",  # اینجا file_id واقعی رو بذار
        "caption": "😂 فیلم کمدی خنده دار",
        "category": "comedy"
    }
]

for movie in movies:
    success = db.add_movie(movie["title"], movie["file_id"], movie["caption"], movie["category"])
    if success:
        print(f"✅ فیلم '{movie['title']}' اضافه شد")
    else:
        print(f"❌ خطا در اضافه کردن فیلم '{movie['title']}'")