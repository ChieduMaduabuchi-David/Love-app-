import json
from Database import *
import threading
import socket
from Userclasses import *
#cretes host socket and listens for users
host = socket.gethostbyname(socket.gethostname())
port = 46830

server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

def init_connect():
    client, address = server.accept()
    client.send('Login'.encode('utf-8'))
    Login = client.recv(1024).decode('utf-8')


    #checks if the user wants to signup or login
    if Login =="False" :
        login_data = client.recv(1024).decode('utf-8')
        login_info = json.loads(login_data)
        result = verify_user(login_info['Username'],login_info['password'])
        match result:
            case 0.0:
                client.send("user not found".encode('utf-8'))
            case 0.1:
                client.send('wrong password'.encode('utf-8'))
            case _:
                client.send('Logged in'.encode('utf-8'))

        print(user_data(result))
    else:
        signup_data = client.recv(1024).decode('utf-8')
        print(signup_data)
        signup_info = json.loads(signup_data)
        username = signup_info['Username']
        password = signup_info['password']
        #reciving users info
        user_in_data = client.recv(1024).decode('utf-8')
        user = User.from_json(user_in_data)
        register_user(user,password)
        print('user created')


        # signup_user(signup_data,user)





# def signup_user(signup_data):
#     user = User()




while True:
    init_connect()

