import socket
from sys import argv
from urllib.parse import urlparse


def parse_header(header):
    for line in header:
        if line.find('Content-Type') != -1:
            if line.find('Content-Type: text/html') == 0:
                return 'wt'
            elif line.find('Content-Type: image/jpeg') == 0:
                return 'wb'
            else:
                raise Exception("UNKNOWN FILE TYPE")


def save_text(filename, body, header_data):
    with open(filename, mode='wt') as b:
        b.write(body)
    with open("index.php.header", mode='wt') as h:
        h.write(header_data)
    print(header_data)


def save_binary(filename, body, header_data):
    with open("bin/{}".format(filename), mode='wb') as b:
        b.write(body)
    print(header_data.decode())


def make_request(url_p, filename="index.php"):
    url = urlparse(url_p)

    crlf = "\r\n"

    request = [
        "GET {} HTTP/1.1".format(url.path),
        "Host: {}".format(url.netloc),
        "Connection: Close",
        "User-Agent: Banic_Awesome_User_Agent",
        "",
        "",
    ]
    # Set up a TCP/IP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect as client to a selected server
    # on a specified port
    s.connect((url.netloc, 80))

    # Protocol exchange - sends and receives
    s.send(crlf.join(request).encode())
    resp = b''
    buffer = s.recv(4096)
    while buffer:
        resp += buffer
        buffer = s.recv(4096)
    header_data, _, body = resp.partition(b'\r\n\r\n')
    mode = parse_header(header_data.decode())
    if mode == 'wt':
        save_text(filename, body.decode(), header_data.decode())
    else:
        save_binary(filename, body, header_data)

    # Close the connection when completed
    s.close()


def main():
    # URL = argv[1]
    url = "http://west.uni-koblenz.de/sites/default/files/styles/personen_bild/public/_IMG0076-Bearbeitet_03.jpg"
    make_request(url, filename="image.jpg")

if __name__ == "__main__":
    main()