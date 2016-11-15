import socket
import json


def Main():
    host = "localhost"
    port = 8080

    mySocket = socket.socket()
    mySocket.bind((host, port))

    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print("Connection from: " + str(addr))
    data = conn.recv(1024).decode()
    if not data:
        return
    user_info = json.loads(data)
    data = 'Name: {}\nAge: {}\nMatrikelnummer: {}'.format(user_info['name'], user_info['age'], user_info['id'])

    print(data)
    conn.close()


if __name__ == '__main__':
    Main()