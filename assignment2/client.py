import socket

def Main():
    host = 'localhost'
    port = 8080

    user_name = input('Insert your name: ')
    user_age = input('Insert your age: ')
    user_id = input('Insert your matrikelnummer: ')

    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = '{}#{}#{}'.format(user_name, user_age, user_id)
    mySocket.send(message.encode())
    data = mySocket.recv(1024).decode()

    print(data)

    mySocket.close()


if __name__ == '__main__':
    Main()