
# coding: utf-8

# # Server

# In[ ]:

import socket
 
def Main():
    host = "localhost"
    port = 8080
     
    mySocket = socket.socket()
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    while True:
        data = conn.recv(1024).decode()
        if not data:
                break
        user_info = str(data).split('#')
        data = 'Name: {}\nAge: {}\nMatrikelnummer: {}'.format(user_info[0],user_info[1],user_info[2])
        conn.send(data.encode())
             
    conn.close()
     
if __name__ == '__main__':
    Main()


# # Client

# In[ ]:

import socket
 
def Main():
    host = 'localhost'
    port = 8080

    user_name = input('Insert your name: ')
    user_age = input('Insert your age: ')
    user_id = input('Insert your matrikelnummer: ')

    mySocket = socket.socket()
    mySocket.connect((host,port))


    while message != 'quit':
        message = '{}#{}#{}'.format(user_name, user_age, user_id)
        mySocket.send(message.encode())
        data = mySocket.recv(1024).decode()

        print (data)

    mySocket.close()
 
if __name__ == '__main__':
    Main()

