import socket
import json
import working_dir.assignment3.our_pars_lib as opl

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
    url = data.strip("\r \n")
    print (
"""Protocol: {};
Domain: {};
Subdomain: {};
Port number: {};
Path:{};
Parameters: {};
Fragment:{}""".format(opl.get_protocol(url),
                      opl.get_domain(url),
                      opl.get_subdomain(opl.get_domain(url)),
                      opl.get_port(url),
                      opl.get_path(url),
                      opl.get_params(url),
                      opl.get_fragment(url)))
    #conn.send(data)  # echo
    #conn.close()