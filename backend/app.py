from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from urllib.parse import quote_plus
import os

app = Flask(__name__)

MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
if not MONGO_PASSWORD:
    raise ValueError("MONGO_PASSWORD environment variable is not set")

encoded_password = quote_plus(MONGO_PASSWORD)

MONGO_URI = f"mongodb+srv://abdullahar0920_db_user:{encoded_password}@abd.b5hva7p.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

db = client['mydatabase']
collection = db['mycollection']

@app.route('/')
def index():
    return render_template('form.html', error=None)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or not email:
            raise ValueError("All fields are required")
        collection.insert_one({"name": name, "email": email})
        return redirect(url_for('success'))
    except Exception as e:
        return render_template('form.html', error=str(e))

@app.route('/success')
def success():
    return "Data submitted successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)