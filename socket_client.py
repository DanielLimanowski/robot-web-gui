""""
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

    return client


def disconnect_from_server(client):
    # always close sockets when finished using them!
    client.close()
    return


def send_command(client):
    print('INFO: Sending request for command...')
    response = ''

    tries = 0
    # keep receiving data from server until we receive an ACK (acknowledge to send command),
    # DEN (deny, do not send command) or we have tried 50 times and failed
    while tries < 1000:
        # send a command request (repeated !) until server responds
        client.sendall('!!!!!!!'.encode())
        tries = tries + 1

    #send a character other than ! to indicate done requesting command
    client.sendall('*'.encode())

    print('INFO: Attempting to get response now...')
    # set MSG_DONTWAIT flag so that the operation is non-blocking
    # ie., check for data and move on - don't wait to receive any

    # make the socket non-blocking so that it doesn't wait for any operation
    client.settimeout(10)

    decoded_resp = ''
    try:
        response = client.recv(4096)
        decoded_resp = response.decode('ascii')
        print('SERVER: Response is: ' + decoded_resp)
    except:
        print('ERROR: Could not get response from server in time...')

    # return to blocking
    client.settimeout(None)

    if decoded_resp == 'ACK':
        print('INFO: Acknowledged request. Sending command...')
        time.sleep(2)
        command = 'this is a:: command$'
        for c in command:
            client.sendall(c.encode())
            print('SENDING: ' + c)
            time.sleep(0.1)

        #client.sendall(b'this is a:: command!')
        print('INFO: Command sent. Exiting.')
    elif response == 'DEN':
        print('INFO: Command request denied. Exiting.')
    else:
        print('ERROR: Server not responding to request. Exiting.')

    # the b in front of the message indicates that the sendall should send the message in byte-form

    return


rover = connect_to_server()

while 1:
    send_command(rover)

disconnect_from_server(rover)

