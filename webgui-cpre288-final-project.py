import eventlet
import socket_client
from flask import Flask, render_template
from flask_socketio import SocketIO, send

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
socketio = SocketIO(app, async_mode='eventlet')

'''
MUST RUN THIS WITH DEBUG MODE OFF OTHERWISE THE SERVER WILL RESTART
AND YOU WILL HAVE ISSUES CONNECTING TO THE ROBOT!!!
'''

# HANDLING USER CONNECTION STATUS
@socketio.on('connect')
def handle_user_connect():
    # broadcast=True sends messages to ALL connected users
    print('User connected.')
    # echo message to all connected users
    send('User connected.', broadcast=True)


# Global variable representing rover robot client (see socket_client.py)
client = socket_client.connect_to_server()


# RECEIVING MESSAGES VIA WEB SOCKETS
@socketio.on('message')
def handle_recv_message(message):
    # broadcast=True sends messages to ALL connected users
    if "User" in message:
        send(message, broadcast=True)
    else:
        send('COMMAND: ' + message, broadcast=True)
        print('Received command: ' + message)
        robot_resp = socket_client.send_command(client, message)
        send(robot_resp, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html')  # TODO - why? -> This gives major errors!!!:, async_mode=socketio.async_mode)


if __name__ == '__main__':
    # The default flask dev server does not support websocket transport
    # Instead we will use the eventlet server, which DOES support websocket transport
    # AND is more appropriate (powerful) for a production setting

    # socketio.run encapsulates the normal app.run() as it needs to in order to take
    # over the typical HTTP request model and replace it with socket communication
    socketio.run(app)  # SEE COMMENT ABOVE!!! , debug=True)