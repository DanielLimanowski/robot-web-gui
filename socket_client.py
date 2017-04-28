"""
A python script to establish a client socket and 
connect to the CPRE 288 Vortex Robot server

@author Daniel Limanowski
"""

import socket
import time


def connect_to_server():
    # establish a new socket for our client (the computer) to connect to the server (VORTEX Robot)
    # using the default parameters (family=AF_INET, type=SOCK_STREAM, protocol=0)
    print('INFO: Setting up the socket...')
    client = socket.socket()

    # hostname/ip address of the server
    host = '192.168.1.1'
    # port of the server
    port = 42880

    # connect to the server using values defined above
    print('INFO: Initializing the connection...')
    client.connect((host, port))

    print('INFO: Successfully connected to robot...')
    return client


def disconnect_from_server(client):
    # always close sockets when finished using them!
    client.close()
    return


def send_command(client, command):
    print('INFO: Sending command: ' + command)
    response = ''

    send_cmd = command + '\0'

    # send command string, max of 50 characters at the moment, including null terminating character
    client.sendall(send_cmd.encode())

    print('INFO: Attempting to get response now...')

    '''
    Since some commands like scan take awhile, there was a need for data collection over a period of time, not
    all at once. The following website inspired the code that follows:
    http://www.binarytides.com/receive-full-data-with-the-recv-socket-function-in-python/
    '''
    cmd_id = send_cmd[0]
    if cmd_id == 's':
        timeout = 18
    elif cmd_id =='m':
        timeout = 4
    elif cmd_id == 't':
        timeout = 3
    elif cmd_id == 'b':
        timeout = 2
    else:
        timeout = 5
    client.setblocking(0)
    total_data = []
    curr_data = ''
    robot_msg = ''

    time_begin = time.time()
    while 1:
        # if we have data fully received
        if total_data and time.time() - time_begin > timeout:
            # Combine all the chunked array data into one string
            robot_msg = 'ROBOT: ' + ''.join(total_data)
            print('ROBOT: ' + ''.join(total_data))
            break
        # if we have NO data and ready to give up
        elif time.time() - time_begin > timeout * 2:
            robot_msg = 'ROBOT - ERROR: Could not get response from server in time...'
            print('ROBOT - ERROR: Could not get response from server in time...')
            break

        # try to receive some data
        try:
            response = client.recv(4096)
            curr_data = response.decode('ascii')
            if curr_data:
                # then data has been received, add to array
                total_data.append(curr_data)
                time_begin = time.time()
            else:
                # wait a tiny bit before querying again
                time.sleep(0.1)
        except:
            pass

    # return to blocking
    client.settimeout(None)

    return robot_msg

# Uncomment the code below to test commands using only this file (WITHOUT the flask app)
'''
rover = connect_to_server()

while 1:
    print('READY FOR COMMAND')
    cmd = input()
    print('SENDING COMMAND')
    send_command(rover, cmd)
    #time.sleep(5)

disconnect_from_server(rover)
'''