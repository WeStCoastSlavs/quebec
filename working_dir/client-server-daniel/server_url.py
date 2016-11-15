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
    url = data.strip("\r \n")
    print("Url: " + url)
    url_dict = {}
    if '#' in url:  # contains fragment?
        url_dict['fragment'] = url.split('#')[1]
        url = url.split('#')[0]
    if '?' in url:  # contains params?
        url_dict['params'] = url.split('?')[1].split('&')
        url = url.split('?')[0]
    colon = url.split(':')
    if (len(colon) == 1):  # no port, no protocol
        url_dict['protocol'] = 'unknown'
        url_dict['domain'] = colon[0].split('/')[0]
        url_dict['path'] = colon[0][len(url_dict['domain']):]
    elif (len(colon) == 2):
        # no port number, or protocol
        if (colon[1][0] == "/"):  # protocol available
            url_dict['protocol'] = colon[0]
            url_dict['port_num'] = 'unknown'
            url_dict['domain'] = colon[1].split('/')[2]
            url_dict['path'] = colon[1][len(url_dict['domain']) + 2:]
        else:  # port num available
            url_dict['port_num'] = colon[1].split('/')[0]
            url_dict['domain'] = colon[0]
            url_dict['path'] = colon[1][len(url_dict['port_num'])]
    elif (len(colon) == 3):
        # with port number
        url_dict['protocol'] = colon[0]
        url_dict['port_num'] = colon[2].split('/')[0]
        url_dict['domain'] = colon[1][2:]
        url_dict['path'] = colon[2][len(url_dict['port_num']):]
    url_dict['subdomains'] = url_dict['domain'].split('.')
    pprint(url_dict)
    conn.close()


if __name__ == '__main__':
    Main()