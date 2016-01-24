"""
Handles the outgoing map, object and
entity data leaving the client host
"""

from socket import socket

# list of client connections
# (sockets)
clients = []

server_socket = None


def init(player_amount):
    global server_socket
    server_socket = socket()
    host = "localhost"
    port = 43244
    server_socket.bind((host, port))

    print("Hosting game on {}:{}".format(host, port))

    server_socket.listen(player_amount)
    con, addr = server_socket.accept()
    print("Connected to {}".format(addr))
    clients.append(con)


def broadcast(msg):
    for client in clients:
        client.send((msg + "\n").encode())
