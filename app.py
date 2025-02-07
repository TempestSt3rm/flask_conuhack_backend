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

#This is the test change 

if __name__ == '__main__':
    app.run(debug=True)