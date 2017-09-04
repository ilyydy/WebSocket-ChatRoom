from flask import session
from flask_socketio import (
    emit,
    join_room,
    leave_room,
    SocketIO
)

socketio = SocketIO()


@socketio.on('join', namespace='/chat')
def join(data):
    print('join', data)
    room = data['room']
    join_room(room)
    session['room'] = room
    name = session.get('name')
    message = '用户:({}) 进入了房间'.format(name)
    d = dict(
        message=message,
    )
    emit('status', d, room=room)


@socketio.on('send', namespace='/chat')
def send(data):
    room = session.get('room')
    name = session.get('name')
    message = data.get('message')
    formatted = '{} : {}'.format(name, message)
    print('send', formatted)
    d = dict(
        message=formatted
    )
    emit('message', d, room=room)


@socketio.on('leave', namespace='/chat')
def leave(data):
    room = session.get('room')
    leave_room(room)
    name = session.get('name')
    d = dict(
        message='{} 离开了房间'.format(name),
    )
    emit('status', d, room=room)
