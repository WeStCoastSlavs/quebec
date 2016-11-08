import socket
import json

name = input("What is your name? \n")
age = input("How old are you? \n")
matrikelnummer = input("What is your Martikelnummer? \n")

pack = {}

pack["name"] = name
pack["age"] = age
pack["matrikelnummer"] = matrikelnummer

pack_json = json.dumps(pack)

TCP_IP = '127.0.0.1'
TCP_PORT = 8080
#BUFFER_SIZE = 1024
MESSAGE = pack_json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
#data = s.recv(BUFFER_SIZE)
s.close()

#print "received data:", data