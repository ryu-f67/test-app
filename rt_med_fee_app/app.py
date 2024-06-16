from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    checkbox_value = data.get('checkbox')
    
    # チェックボックスの状態に応じた処理をここに追加
    response_data = {"message": "Checkbox is " + ("checked" if checkbox_value else "unchecked")}
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
