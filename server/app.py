import random
import string

import flask
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)

socket_io = SocketIO(app)

op_codes = {}
opponent = {}
reset = {}


@app.route('/api/getId')
def get_id():
    return {'id_code': ''.join(random.sample(string.digits, k=4))}


@socket_io.on('initRoom', namespace='/socket.io')
def init_room(data):
    room = data
    join_room(room)
    op_codes[room] = -1
    print(room)


@socket_io.on('invite', namespace='/socket.io')
def invite(data):
    print(data)
    my_id = data['myId']
    op_id = data['opId']
    socket_io.emit('recvInvitation', my_id, namespace='/socket.io', room=op_id)


@socket_io.on('accept', namespace='/socket.io')
def accept(data):
    print(data)
    my_id = data['myId']
    op_id = data['opId']
    join_room(op_id)
    opponent[op_id] = my_id
    opponent[my_id] = op_id
    socket_io.emit('startGame', my_id, namespace='/socket.io', room=op_id)


@socket_io.on('sendOpcode', namespace='/socket.io')
def send_op_code(data):
    room = data['room']
    my_id = data['myId']
    op_codes[my_id] = data['code']
    op_id = opponent[my_id]
    if op_codes[op_id] == -1:
        socket_io.emit('startShortCountDown', my_id, namespace='/socket.io', room=room)
        print(f'one op from {my_id}, which is {data["code"]}')
    else:
        socket_io.emit('recvOpcode', {'code1': op_codes[my_id], 'code2': op_codes[op_id], 'id1': my_id},
                       namespace='/socket.io', room=room)
        print(f'two codes are {op_codes[my_id]}, {op_codes[op_id]}')
        op_codes[my_id] = -1
        op_codes[op_id] = -1


@socket_io.on('reset', namespace='/socket.io')
def init(data):
    room = data['room']
    if room not in reset:
        print('one')
        reset[room] = 1
    else:
        socket_io.emit('startGame', '', namespace='/socket.io', room=room)
        del reset[room]


if __name__ == '__main__':
    socket_io.run(app)
