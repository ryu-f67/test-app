from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

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
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO records (category, amount, description, notes) VALUES (?, ?, ?, ?)',
                   (data['category'], data['amount'], data['description'], data['notes']))
    conn.commit()
    conn.close()
    return '', 201

@app.route('/api/records/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE records SET category=?, amount=?, description=?, notes=? WHERE id=?',
                   (data['category'], data['amount'], data['description'], data['notes'], record_id))
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


if __name__ == '__main__':
    app.run(debug=True)
