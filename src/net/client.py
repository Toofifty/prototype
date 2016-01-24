from socket import socket

client_socket = None


def init(host, port):
    print("Attempting to connect to {}:{}".format(host, port))

    global client_socket
    client_socket = socket()
    client_socket.connect((host, port))


def send(msg):
    print("sent", msg)

    global client_socket
    client_socket.send((msg + "\n").encode())
