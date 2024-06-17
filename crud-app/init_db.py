# init_db.py
import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    notes TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
