import json
import threading
import socket
import Userclasses
#cretes host socket and listens for users
host = socket.gethostbyname(socket.gethostname())
port = 46830

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

def init_connect():
    client, address = server.accept()
    client.send('Login'.encode('utf-8'))
    signup = client.recv(1024).decode('utf-8')


    #checks if the user wants to signup or login
    if signup=="True":
        signup_data = client.recv(1024).decode('utf-8')
        signup_user(signup_data)
    else :
        login_data = client.recv(1024).decode('utf-8')
        login_info = json.loads(login_data)
        print(type(login_info))

def signup_user(signup_data):
    user = User()




while True:
    init_connect()

