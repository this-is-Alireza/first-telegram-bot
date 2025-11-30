import sqlite3
from database import MovieDatabase

class MovieDatabaseExtensions(MovieDatabase):
    """افزونه‌های جدید برای دیتابیس بدون تغییر در کلاس اصلی"""
    
    def get_movie_download_count(self, movie_id):
        """دریافت تعداد دانلودهای یک فیلم"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT download_count FROM movies WHERE id = ?', 
                (movie_id,)
            )
            result = cursor.fetchone()
            return result[0] if result else 0
    
    def get_movie_by_id(self, movie_id):
        """دریافت اطلاعات یک فیلم بر اساس ID"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                'SELECT * FROM movies WHERE id = ?', 
                (movie_id,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'file_id': row[2],
                    'caption': row[3],
                    'category': row[4],
                    'download_count': row[5]
                }
            return None
    
    def delete_movie(self, movie_id):
        """حذف یک فیلم از دیتابیس"""
        try:
            with self.get_connection() as conn:
                conn.execute('DELETE FROM movies WHERE id = ?', (movie_id,))
                conn.commit()
                return True
        except sqlite3.Error:
            return False
    
    def increment_download_count(self, movie_id):
        """افزایش تعداد دانلود یک فیلم"""
        with self.get_connection() as conn:
            conn.execute(
                'UPDATE movies SET download_count = download_count + 1 WHERE id = ?',
                (movie_id,)
            )
            conn.commit()