from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import os

DATABASE_URL = os.getenv('DATABASE_URL')

@app.route('/')
def home():
    return jsonify({"message": "Hello from Flask on Vercel!"})

def retrieve_user(email):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    user_email = email
    select_sql = """
    SELECT id, email FROM "user" WHERE email = %s;
    """
    cur.execute(select_sql, (user_email,))
    user_info = cur.fetchone()
    try:
        if user_info:
            return {
                "id": user_info[0],
                "email": user_info[1]
            }
        else:
            return None
    except:
        pass
    finally:
        cur.close()
        conn.close()
    
    
@app.route('/get_user', methods=['GET'])
def get_user():
    email = request.args.get('email')
    if not email:
        return jsonify({'error': 'Email parameter is required'}), 400

    user_data = retrieve_user(email)
    
    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Vercel requires this
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True)

