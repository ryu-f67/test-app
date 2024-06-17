from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/records', methods=['GET', 'POST'])
def manage_records():
    if request.method == 'POST':
        data = request.json
        category = data['category']
        amount = data['amount']
        description = data['description']
        notes = data['notes']
        
        conn = connect_db()
        c = conn.cursor()
        c.execute("INSERT INTO records (category, amount, description, notes) VALUES (?, ?, ?, ?)",
                  (category, amount, description, notes))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 201

    elif request.method == 'GET':
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM records")
        records = c.fetchall()
        conn.close()
        return jsonify(records), 200

@app.route('/api/records/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_record(id):
    if request.method == 'PUT':
        data = request.json
        category = data['category']
        amount = data['amount']
        description = data['description']
        notes = data['notes']
        
        conn = connect_db()
        c = conn.cursor()
        c.execute("UPDATE records SET category = ?, amount = ?, description = ?, notes = ? WHERE id = ?",
                  (category, amount, description, notes, id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200

    elif request.method == 'DELETE':
        conn = connect_db()
        c = conn.cursor()
        c.execute("DELETE FROM records WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
