import socket
import json
from pprint import pprint


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
    uri = user_info['url']
    url = {}
    if '#' in uri:
        url['fragment'] = uri.split('#')[1]
        uri = uri.split('#')[0]
    if '?' in uri:
        url['params'] = uri.split('?')[1].split('&')
        uri = uri.split('?')[0]
    colon = uri.split(':')
    url['protocol'] = colon[0]
    if (len(colon) == 2):
        # no port number
        url['domain'] = colon[1].split('/')[2]
        url['path'] = colon[1][len(url['domain']) + 2:]
    else:
        # with port number
        url['port_num'] = colon[2].split('/')[0]
        url['domain'] = colon[1][2:]
        url['path'] = colon[2][len(url['port_num']):]
    url['subdomain'] = url['domain'].split('.')
    pprint(url)
    conn.close()


if __name__ == '__main__':
    Main()