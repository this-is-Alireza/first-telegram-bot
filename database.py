import sqlite3
import logging

logger = logging.getLogger(__name__)

class MovieDatabase:
    def __init__(self, db_path='movies.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS movies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL UNIQUE,
                    file_id TEXT NOT NULL UNIQUE,
                    caption TEXT,
                    category TEXT DEFAULT 'general',
                    download_count INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    requests_today INTEGER DEFAULT 0,
                    total_requests INTEGER DEFAULT 0,
                    last_request_date DATE,
                    is_premium BOOLEAN DEFAULT FALSE,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_movie(self, title, file_id, caption="", category="general"):
        try:
            with self.get_connection() as conn:
                conn.execute('''
                    INSERT INTO movies (title, file_id, caption, category)
                    VALUES (?, ?, ?, ?)
                ''', (title, file_id, caption, category))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_movies(self):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM movies WHERE is_active = TRUE ORDER BY title')
            movies = []
            for row in cursor.fetchall():
                movies.append({
                    'id': row[0],
                    'title': row[1],
                    'file_id': row[2],
                    'caption': row[3],
                    'category': row[4]
                })
            return movies
    
    def add_user(self, user_id, username, first_name, last_name):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            conn.commit()