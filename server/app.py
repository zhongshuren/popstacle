from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)

socket_io = SocketIO(app)

unused_id = set(range(10000))
total_count = 0
used_id = set()
sid_id = {}
op_codes = {}
opponent = {}
reset_id = {}


@app.route('/')
def index():
    global total_count
    total_count += 1
    return render_template('index.html')


@app.route('/api/getPlayerCount')
def get_player_count():
    return {'count': 10000 - len(unused_id)}


@app.route('/api/getTotalCount')
def get_total_count():
    return {'count': total_count}


@app.route('/api/getId')
def get_id():
    try:
        el = unused_id.pop()
        unused_id.add(el)
        data = {'id_code': str(el).zfill(4)}
        return data
    finally:
        pass


@socket_io.on('initRoom', namespace='/socket.io')
def init_room(data):
    try:
        if len(str(data)) != 4:
            pass
        room = data
        op_codes[room] = -1
        if int(room) in used_id:
            join_room(request.sid)
            socket_io.emit('refresh', '', namespace='/socket.io', room=request.sid)
        else:
            join_room(room)
            unused_id.remove(int(room))
            used_id.add(int(room))
            sid_id[request.sid] = room
    finally:
        pass


@socket_io.on('invite', namespace='/socket.io')
def invite(data):
    try:
        my_id = data['myId']
        op_id = data['opId']
        socket_io.emit('recvInvitation', my_id, namespace='/socket.io', room=op_id)
    finally:
        pass


@socket_io.on('accept', namespace='/socket.io')
def accept(data):
    try:
        my_id = data['myId']
        op_id = data['opId']
        leave_room(my_id)
        join_room(op_id)
        opponent[op_id] = my_id
        opponent[my_id] = op_id
        socket_io.emit('startGame', my_id, namespace='/socket.io', room=op_id)
    finally:
        pass


@socket_io.on('sendOpcode', namespace='/socket.io')
def send_op_code(data):
    try:
        room = data['room']
        my_id = data['myId']
        op_codes[my_id] = data['code']
        op_id = opponent[my_id]
        if op_codes[op_id] == -1:
            socket_io.emit('startShortCountDown', my_id, namespace='/socket.io', room=room)
            # print(f'one op from {my_id}, which is {data["code"]}')
        else:
            socket_io.emit('recvOpcode', {'code1': op_codes[my_id], 'code2': op_codes[op_id], 'id1': my_id},
                           namespace='/socket.io', room=room)
            # print(f'two codes are {op_codes[my_id]}, {op_codes[op_id]}')
            op_codes[my_id] = -1
            op_codes[op_id] = -1
    finally:
        pass


@socket_io.on('reset', namespace='/socket.io')
def reset(data):
    try:
        room = data['room']
        if room not in reset_id:
            reset_id[room] = 1
        else:
            socket_io.emit('startGame', '', namespace='/socket.io', room=room)
            del reset_id[room]
    finally:
        pass


@socket_io.on('disconnect', namespace='/socket.io')
def disconnect():
    try:
        if request.sid in sid_id:
            # print('disconnected')
            room = sid_id[request.sid]
            del sid_id[request.sid]
            unused_id.add(int(room))
            used_id.remove(int(room))
    finally:
        pass


if __name__ == '__main__':
    socket_io.run(app, debug=False)
