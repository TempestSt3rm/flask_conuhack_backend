import os
from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Get database URL from Railway
DATABASE_URL = os.getenv('DATABASE_URL')

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask on Railway!"})

@app.route('/get_user', methods=['GET'])
def get_user():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('SELECT id, email FROM "user" WHERE email = %s;', (email,))
    user_info = cur.fetchone()
    cur.close()
    conn.close()

    if user_info:
        return jsonify({"id": user_info[0], "email": user_info[1]}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)