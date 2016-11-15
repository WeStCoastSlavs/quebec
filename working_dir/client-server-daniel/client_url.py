import socket, json

def Main():
    host = 'localhost'
    port = 8080

    user_url = input('Insert URL for parsing: ')

    mySocket = socket.socket()
    mySocket.connect((host, port))

    # message = dict({'url': user_url})
    message = user_url + "\r \n"
    mySocket.send(message.encode())

    print(message)

    mySocket.close()


if __name__ == '__main__':
    Main()