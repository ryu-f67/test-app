from datetime import datetime

from flask import Flask, request, jsonify, render_template
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

@app.route('/database')
def database_list():
    return render_template('database.html')

@app.route('/api/records', methods=['GET'])
def get_records():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM records')
    records = cursor.fetchall()
    conn.close()
    return jsonify(records)

@app.route('/api/records', methods=['POST'])
def add_record():
    data = request.json
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO records (name, category, point, update_time) VALUES (?, ?, ?, ?)',
                   (data['name'], data['category'], data['point'], update_time))
    conn.commit()
    conn.close()
    return '', 201

@app.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.json
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE records SET name=?, category=?, point=?, update_time=? WHERE id=?',
                   (data['name'], data['category'], data['point'], update_time, record_id))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/records/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM records WHERE id=?', (record_id,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/reorder', methods=['POST'])
def reorder_records():
    data = request.json
    new_order = data['order']
    conn = get_db()
    cursor = conn.cursor()
    
    # Perform updates in a transaction for safety
    try:
        for index, record_id in enumerate(new_order, start=1):
            cursor.execute('UPDATE records SET sort_order=? WHERE id=?', (index, record_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
    
    return '', 204

@app.route('/result')
def result():
    results = request.args.getlist('results')
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
