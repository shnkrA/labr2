import os
import time
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "appdb")
DB_USER = os.getenv("POSTGRES_USER", "appuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secretpassword")

def get_db_connection():
    # Просте підключення до БД з повторними спробами
    for _ in range(5):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except psycopg2.OperationalError:
            time.sleep(2)
    raise Exception("Cannot connect to Database")

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL
            );
        ''')
        cur.execute('SELECT COUNT(*) FROM users;')
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO users (name, email) VALUES ('Олексій', 'alex@example.com'), ('Марія', 'maria@example.com');")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "service": "Service A (Backend)",
        "version": "1.0.0",
        "status": "Running"
    }), 200

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email FROM users;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(users), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)