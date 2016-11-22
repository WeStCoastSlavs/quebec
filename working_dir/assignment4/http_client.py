# -*- coding: utf-8 -*-
from sys import argv
import socket
from urllib.parse import urlparse

script, url = argv

#parsing url
parsed_url = urlparse(url)
#print(parsed_url)
host = parsed_url.netloc
#print(host)
# making socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host , 80))
message = b"GET "+parsed_url.path.encode()+b" HTTP/1.0\r\n\r\n"
s.send(message)
#while True:

temp_file = open('temp.php', 'wb')

while True:
    resp = s.recv(1024)
    if resp == b"": break
    temp_file.write(resp)
    #print(response)
temp_file.close()
# Close the connection when completered

#print ("HEADER:\n"+header_content)
#print ("body:\n"+body_content)

#resp.partition()
s.close()

temp = open("temp.php", "rb")

body = open('index.php', 'wb')

is_body = False
for line in temp:
    if line.isspace() and is_body == False:
        is_body = True
    elif is_body == False:
        header.write(line)
        header.flush()
    else:
        body.write(line)
        body.flush()

header.close()
body.close()

# header.write(header_content)
# index.write(body_content)

#  http://west.uni-koblenz.de/en/studying/courses/ws1617/introduction-to-web-science
#  http://west.uni-koblenz.de/sites/default/files/styles/personen\_bild/public/\_IMG0076-Bearbeitet\_03.jpg

# python httpclient.py http://west.uni-koblenz.de/index.php
#
# HTTP/1.1 200 OK
# Date: Wed, 16 Nov 2016 13:19:19 GMT
# Server: Apache/2.4.7 (Ubuntu)
# X-Powered-By: PHP/5.5.9-1ubuntu4.20
# X-Drupal-Cache: HIT
# Etag: "1479302344-0"
# Content-Language: de
# X-Frame-Options: SAMEORIGIN
# X-UA-Compatible: IE=edge,chrome=1
# X-Generator: Drupal 7 (http://drupal.org)
# Link: <http://west.uni-koblenz.de/de>; rel="canonical",<http://west.uni-koblenz.de/de>; rel="shortlink"
# Cache-Control: public, max-age=0
# Last-Modified: Wed, 16 Nov 2016 13:19:04 GMT
# Expires: Sun, 19 Nov 1978 05:00:00 GMT
# Vary: Cookie,Accept-Encoding
# Connection: close
# Content-Type: text/html; charset=utf-8