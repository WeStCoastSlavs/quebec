import socket, json

def Main():
    host = 'localhost'
    port = 8080

    user_name = input('Insert your name: ')
    user_age = input('Insert your age: ')
    user_id = input('Insert your matrikelnummer: ')

    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = dict({'name' : user_name, 'age': user_age, 'id': user_id})
    mySocket.send(json.dumps(message).encode())

    print(message)

    mySocket.close()


if __name__ == '__main__':
    Main()