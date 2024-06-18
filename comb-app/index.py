from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

# データベースからアイテムをカテゴリごとに取得
def get_records_by_category(category):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, point FROM records WHERE category = ?', (category,))
    records = cursor.fetchall()
    conn.close()
    return records

# チェックボックスに対応する情報を保持
info_data = {f"checkbox{i}": f"情報{i}" for i in range(1, 31)}

@app.route('/')
def index():
    records_a = get_records_by_category('照射方法')
    records_b = get_records_by_category('加算')
    records_c = get_records_by_category('管理')
    return render_template('index.html', records_a=records_a, records_b=records_b, records_c=records_c)

@app.route('/get_info_and_scores', methods=['POST'])
def get_info_and_scores():
    selected_ids = request.json.get('selected_ids', [])
    conn = get_db()
    cursor = conn.cursor()
    info_scores = []
    for item_id in selected_ids:
        cursor.execute('SELECT name, point FROM records WHERE id = ?', (int(item_id[8:]),))  # checkbox の id から id を取得
        name, point = cursor.fetchone()
        info_scores.append({"info": name, "point": point})
    conn.close()
    return jsonify(info_scores)

if __name__ == '__main__':
    app.run(debug=True)
