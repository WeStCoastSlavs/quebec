import socket, json

def Main():
    host = 'localhost'
    port = 8080

    user_url = input('Insert URL for parsing: ')

    mySocket = socket.socket()
    mySocket.connect((host, port))

    message = dict({'url': user_url})
    mySocket.send(json.dumps(message).encode())

    print(message)

    mySocket.close()


if __name__ == '__main__':
    Main()