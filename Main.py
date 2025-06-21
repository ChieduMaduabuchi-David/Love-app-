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

def init_connect(client_socket, address):
    client_socket.send('Login'.encode('utf-8'))
    signup = client_socket.recv(1024).decode('utf-8')


    #checks if the user wants to signup or login
    # for sign up
    if signup == 'True':
        signup_data = client_socket.recv(1024).decode('utf-8')

        signup_info = json.loads(signup_data)
        # username = signup_info['Username'] #doesn't use
        password = signup_info['password']

        #reciving users info
        user_in_data = client_socket.recv(1024).decode('utf-8')
        try:
            user = User.from_json(user_in_data)
        except ValueError:
            client_socket.send("ERORR: bad data".encode('utf-8'))
            return

        responce=register_user(user,password)
        responce= str(responce)
        client_socket.send(responce.encode('utf-8'))

    #for login
    elif signup == 'False':
        login_data = client_socket.recv(1024).decode('utf-8')

        login_info = json.loads(login_data)
        result = verify_user(login_info['Username'], login_info['password'])
        match result:
            case 0.0:
                client_socket.send("user not found".encode('utf-8'))
            case 0.1:
                client_socket.send('wrong password'.encode('utf-8'))
            case _:
                client_socket.send('Logged in'.encode('utf-8'))
                activate_user(client_socket, login_data)
        # print(user_data(result))

def activate_user(client_socket,login_data):
    pass





while True:
    try:
        client, address = server.accept()
        threading.Thread(target=init_connect, args=(client, address)).start()
    except Exception as e:
        print(f"[SERVER ERROR] {e}")

        # signup_user(signup_data,user)









