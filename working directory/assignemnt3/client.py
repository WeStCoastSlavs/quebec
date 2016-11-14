import socket
import json

url = input("Enter your URL: \n")

url = url+"\r \n"

TCP_IP = '127.0.0.1'
TCP_PORT = 8080
#BUFFER_SIZE = 1024
MESSAGE = url

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE.encode())
#data = s.recv(BUFFER_SIZE)
s.close()

#print "received data:", data