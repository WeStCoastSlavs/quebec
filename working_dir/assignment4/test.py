from urllib.parse import urlparse
import socket, sys

script, url = sys.argv
# Set up a TCP/IP socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
parsed_url = urlparse(url)
# Connect as client to a selected server
# on a specified port
s.connect((url,80))

# Protocol exchange - sends and receives
s.send("GET /en/studying/courses/ws1617/introduction-to-web-science HTTP/1.0\r\n\r\n".encode('utf-8'))
while True:
        resp = s.recv(1024).decode('utf-8')
        if resp == "": break
        print(resp)

# Close the connection when completed
s.close()
print("\ndone")
