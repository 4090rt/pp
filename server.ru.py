from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Создание таблицы при первом запуске
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, password, email) VALUES (?, ?, ?)', (name, password, email))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, name, email FROM users')
    users = c.fetchall()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
