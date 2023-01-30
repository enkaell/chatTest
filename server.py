import logging

import eventlet
import socketio
import datetime
from utils import check_valid_token, get_chat_name_by_id

sio = socketio.Server()
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit("User", sid)


@sio.on('message')
def on_message(sid, data: dict):
    if "Bearer" in data.keys() and check_valid_token(data["Bearer"]):
        if "message" in data.keys():
            sio.emit('message', {"message": data['message'], "time": str(datetime.datetime.now())})
            print(f"{sid} sent a message")
        elif "chat_id" in data.keys():
            sio.enter_room(sid, get_chat_name_by_id(data["chat_id"]))
            print(f"{sid} joined in a chat")
    else:
        print(f"{sid} is not authorized")
        sio.emit('message', {'message': 'Not authorized'}, to=sid)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
