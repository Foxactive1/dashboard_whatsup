from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'mensagens.json')

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
