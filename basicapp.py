from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return 'hello world'

@socketio.on('message')
def handle_message(data):
    print('received message')

@socketio.on('my event', namespace='/test')
def test_message(message):
    print("My event")
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@app.route('/test')
def socket():
    return  render_template('basicsocket.html') #, var1=value1, ...

@app.route('/response')
def retstuff():
    num_list = [1,2,3,4,5]
    num_dict = {'numbers' : num_list, 'name' : 'Numbers'}
    #returns {'output' : {'numbers' : [1,2,3,4,5], 'name' : 'Numbers'}}
    return json.dumps({'output' : num_dict})

if __name__ == "__main__":

    socketio.run(app, debug=True)