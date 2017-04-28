import eventlet
from flask import Flask, render_template
from flask_socketio import SocketIO, send

eventlet.monkey_patch()
import socket_client

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
        if robot_resp[12] == 'p':
            # then we must parse scan input starting at the first 'd'
            robot_data = robot_resp[7:]
            parse_scan(robot_data)

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

'''
Parses the data received from the scan command
'''


def parse_scan(data):
    print('Data: ' + data)
    # now we have the raw input. take the code line by line (90 in total)
    index = 0
    end_index = 0
    lines_arr = data.split(';')
    print(lines_arr[60])
    print(lines_arr[88])

    ping_arr = []
    ir_arr = []
    deg_arr = []

    curr_line_num = 0
    while curr_line_num < 90:
        curr_line = lines_arr[curr_line_num]

        print('CURR LINE: ' + curr_line)

        line_index = 0

        while curr_line[line_index].isdigit() == False:
            line_index += 1;

        end_index = line_index

        while curr_line[end_index] != ',':
            end_index += 1

        deg_arr[curr_line_num] = curr_line[line_index:end_index]
        print(deg_arr[curr_line_num])

        '''
        while curr_line[line_index] != 'p':
            print(curr_line[line_index])
            line_index += 1
        line_index += 1
        line_index += 1
        end_index = line_index
        while curr_line[end_index] != ',':
            end_index += 1
        ping_arr[curr_line_num] = curr_line[line_index:end_index]
        line_index = end_index
        while curr_line[line_index] != 'i':
            line_index += 1
        line_index += 1;
        line_index += 1;
        ir_arr[curr_line_num] = curr_line[line_index:]

        '''
        curr_line_num += 1
