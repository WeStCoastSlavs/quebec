import socket
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 8080
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#print "Socket initialized"
s.bind((TCP_IP, TCP_PORT))
s.listen(5)


#print "waiting for clients"
conn, addr = s.accept()

#print 'Connection address:', addr
while True:
    data = conn.recv(BUFFER_SIZE).decode()
    if not data: break
    pack = json.loads(data)
    print ("""Name: {};
Age: {};
Matrikelnummer: {};""".format(pack["name"],pack["age"], pack["matrikelnummer"]))
    #conn.send(data)  # echo
    #conn.close()