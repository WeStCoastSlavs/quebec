import socket


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
    user_info = str(data).split('#')
    data = 'Name: {}\nAge: {}\nMatrikelnummer: {}'.format(user_info[0], user_info[1], user_info[2])
    conn.send(data.encode())

    conn.close()


if __name__ == '__main__':
    Main()