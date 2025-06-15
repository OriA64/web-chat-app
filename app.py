from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
import os
from firebase_config import FIREBASE_CONFIG

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret!')

# Initialize Firebase
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_CONFIG['databaseURL']
})

# Reference to the messages in Firebase
messages_ref = db.reference('messages')
users_ref = db.reference('users')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages')
def get_messages():
    messages = messages_ref.get() or []
    return {'messages': messages}

@app.route('/users')
def get_users():
    users = users_ref.get() or []
    return {'users': users}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
