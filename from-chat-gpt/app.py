from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# データベースからアイテムをカテゴリごとに取得
def get_items_by_category(category):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, point FROM items WHERE category = ?', (category,))
    items = cursor.fetchall()
    conn.close()
    return items

# チェックボックスに対応する情報を保持
info_data = {f"checkbox{i}": f"情報{i}" for i in range(1, 31)}

@app.route('/')
def index():
    items_a = get_items_by_category('A')
    items_b = get_items_by_category('B')
    items_c = get_items_by_category('C')
    return render_template('index.html', items_a=items_a, items_b=items_b, items_c=items_c)

@app.route('/get_info_and_scores', methods=['POST'])
def get_info_and_scores():
    selected_ids = request.json.get('selected_ids', [])
    conn = get_db()
    cursor = conn.cursor()
    info_scores = []
    for item_id in selected_ids:
        cursor.execute('SELECT name, score FROM items WHERE id = ?', (int(item_id[8:]),))  # checkbox の id から id を取得
        name, score = cursor.fetchone()
        info_scores.append({"info": name, "score": score})
    conn.close()
    return jsonify(info_scores)

if __name__ == '__main__':
    app.run(debug=True)
