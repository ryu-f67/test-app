# init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    point INTEGER NOT NULL,
                    update_time TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
