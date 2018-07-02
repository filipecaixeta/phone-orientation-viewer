from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit
import socket
from struct import *
import requests
from threading import Lock
import os
import eventlet
import os

if os.name == 'nt':
    eventlet.monkey_patch(os=False)
else:
    eventlet.monkey_patch()

UDP_IP = str(os.environ['UDP_IP'])
UDP_PORT = 6000
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

thread = None
thread_lock = Lock()
SOCK = None
print("Receiver IP: ", UDP_IP)
print("Port: ", UDP_PORT)

@app.route('/')
def index():
    return send_from_directory('static','index.html')

@socketio.on('connect', namespace='/sensors')
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=startUdp)

@socketio.on('disconnect', namespace='/sensors')
def disconnect():
    pass

def toDict1(data):
    d = {}
    d['Acceleration'] = unpack_from('!fff', data, 0)
    d['Gravity'] = unpack_from('!fff', data, 4*3)
    d['Rotation Rate'] = unpack_from('!fff', data, 4*6)
    d['Orientation'] = unpack_from('!fff', data, 4*9)
    d['Ambient Light'] = unpack_from('!f', data, 4*14)
    d['Proximity'] = unpack_from('!f', data, 4*15)
    return d

def toDict2(data):
    d = {}
    data = [float(i) for i in str(data)[2:-5].split(",")]
    d['Orientation'] = data
    return d

def startUdp():
        global UDP_IP
        global UDP_PORT
        global SOCK
        SOCK = socket.socket(socket.AF_INET,
                    socket.SOCK_DGRAM)
        SOCK.bind((UDP_IP, UDP_PORT))
        print("Reciving from sensors")
        while True:
            data, addr = SOCK.recvfrom(1024)
            d = toDict2(data)
            socketio.emit('sensors', d, broadcast=True, namespace='/sensors')

if __name__ == '__main__':
    socketio.run(app, debug=False, port=80, host="0.0.0.0")
