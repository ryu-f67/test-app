import sqlite3

# データベースの接続とテーブル作成
conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        score INTEGER NOT NULL DEFAULT 0
    )
''')

# 既存データの削除
c.execute('DELETE FROM items')

# 30個のサンプルデータの挿入
items = [
    ('アイテム1', 'A', 80),
    ('アイテム2', 'B', 75),
    ('アイテム3', 'C', 90),
    ('アイテム4', 'A', 85),
    ('アイテム5', 'B', 88),
    ('アイテム6', 'C', 92),
    ('アイテム7', 'A', 78),
    ('アイテム8', 'B', 82),
    ('アイテム9', 'C', 89),
    ('アイテム10', 'A', 83),
    ('アイテム11', 'B', 77),
    ('アイテム12', 'C', 91),
    ('アイテム13', 'A', 79),
    ('アイテム14', 'B', 84),
    ('アイテム15', 'C', 87),
    ('アイテム16', 'A', 86),
    ('アイテム17', 'B', 81),
    ('アイテム18', 'C', 93),
    ('アイテム19', 'A', 88),
    ('アイテム20', 'B', 79),
    ('アイテム21', 'C', 94),
    ('アイテム22', 'A', 82),
    ('アイテム23', 'B', 85),
    ('アイテム24', 'C', 90),
    ('アイテム25', 'A', 87),
    ('アイテム26', 'B', 80),
    ('アイテム27', 'C', 95),
    ('アイテム28', 'A', 84),
    ('アイテム29', 'B', 83),
    ('アイテム30', 'C', 92),
]

c.executemany('INSERT INTO items (name, category, score) VALUES (?, ?, ?)', items)
conn.commit()
conn.close()
