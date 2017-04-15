
""""
A python script to establish a client socket and 
connect to the CPRE 288 Vortex Robot server

@author Daniel Limanowski
"""

import socket

# establish a new socket for our client (the computer) to connect to the server (VORTEX Robot)
client = socket.socket()
# hostname/ip address of the server
host = '192.168.1.1'
# port of the server
port = 42880

# connect to the server using values defined above
client.connect(host, port)

print(client.recv(1024))

# always close sockets when finished using them!
client.close()




