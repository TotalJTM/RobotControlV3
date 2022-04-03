from flask import Flask, render_template, session
from flask_session import Session
from flask_socketio import SocketIO, emit, send
import json
import time
import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

socketio = SocketIO(app, manage_session=False)

sensors_dict = {
           's1': {   
                'Value 1':10,
            },
            's2': {   
                'Value 2':10,
            },
            's3': {   
                'Value 3':0,
            },
            's4': {
                'Value 4':0,
            },
}

def format_sensor_dict():
    d = sensors_dict
    #print(d)
    #for i in d['sensors']:
    #    print(i)
        #i['value'] = str(i['value'])
    #print(d)
    return d

thread_flag = True

def adjust_values():
    counter = 0
    print("thread Started")
    while thread_flag:
        for key in sensors_dict:
            for val in sensors_dict[key]:
                sensors_dict[key][val] = str(counter)
            
        counter += 1
        socketio.emit('update', format_sensor_dict())
        #print(sensors_dict)
        time.sleep(0.5)

@app.route('/')
def index():
    d = format_sensor_dict()
    session['sensors'] = d
    th.start()
    return render_template('sensordash.html', data=d)

th = threading.Thread(target=adjust_values)

if __name__ == "__main__":

    try:
        socketio.run(app)
        th.start()

    except KeyboardInterrupt:
        thread_flag = False