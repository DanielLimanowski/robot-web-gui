from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'password'
socketio = SocketIO(app, async_mode='eventlet')


# RECEIVING MESSAGES VIA WEB SOCKETS
@socketio.on('message')
def handle_recv_message(message):
    # broadcast=True sends messages to ALL connected users
    print('Received message: ' + message)
    # echo message to all connected users
    send(message, broadcast=True)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


if __name__ == '__main__':
    # The default flask dev server does not support websocket transport
    # Instead we will use the eventlet server, which DOES support websocket transport
    # AND is more appropriate (powerful) for a production setting

    # socketio.run encapsulates the normal app.run() as it needs to in order to take
    # over the typical HTTP request model and replace it with socket communication
    socketio.run(app, debug=True)
