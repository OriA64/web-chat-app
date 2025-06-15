from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret!')
socketio = SocketIO(app)

# Store connected clients and their nicknames
connected_clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('register_nickname')
def handle_nickname(data):
    nickname = data['nickname']
    connected_clients[request.sid] = nickname
    emit('nickname_registered', {'nickname': nickname})
    emit('user_joined', {'nickname': nickname}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    nickname = connected_clients[request.sid]
    emit('receive_message', {'nickname': nickname, 'message': message}, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, debug=True, host='0.0.0.0', port=port)
