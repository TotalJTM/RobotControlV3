from flask import Flask, render_template, session
from flask_session import Session
from flask_socketio import SocketIO, emit, send
import json
import time
import threading

@app.route('/')
def index():
    d = format_sensor_dict()
    session['sensors'] = d
    th.start()
    return render_template('sensordash.html', data=d)