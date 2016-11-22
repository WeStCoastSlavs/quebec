# -*- coding: utf-8 -*-
import socket
import re

# Set up a TCP/IP socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science
# Connect as client to a selected server
# on a specified port
s.connect(("west.uni-koblenz.de",80))

# Protocol exchange - sends and receives
s.send("GET /en/studying/courses/ws1617/introduction-to-web-science HTTP/1.0\n\n".encode())
response = ""
while True:
        resp = s.recv(1024)
        if resp == b"": break
        response += resp.decode()
print (response.count("<img"))
# Close the connection when completed
s.close()

def substrings(string, first, last):
    substring_list = []

    while True:
        index = string.find(first)
        if index == -1:
            break
        string = string[index+len(first):]
        end_sub = string.find(last)
        substring = first+string[:end_sub+len(last)]
        print(substring)
        string = string[end_sub+len(last):]
        substring_list.append(substring)
    return substring_list

def strip_front_back(string, front, back):
    return string.strip(front).strip(back)

img_tags = "".join(substrings(response,"<img", "/>"))
print(img_tags)
print(substrings(img_tags, 'src="', '"'))
src_list = substrings(img_tags, 'src="', '"')
list_src = []
for src in src_list:
    x = strip_front_back(src,'src="', '"')
    list_src.append(x)
print(list_src)