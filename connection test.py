import socket
import datetime
import pytz
import time
import json

host = socket.gethostbyname(socket.gethostname())
port = 46830


self_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        self_socket.connect((host,port))
        break
    except ConnectionRefusedError:
        continue

message = self_socket.recv(1024).decode('utf-8')

#Username and password will be properly implemented in the client side
username="thomas"
password='123qwe'

#cheking letting the server know the user wants to login

def test_firs_interaction(opt):

    if message == 'Login' and opt == 1:
        self_socket.send('False'.encode('utf-8'))

        #creating login details
        login_details_dict={'Username':username,'password':None}

        # sending login details
        login_details = json.dumps(login_details_dict)
        self_socket.send(login_details.encode('utf-8'))
    else:
        self_socket.send('True'.encode('utf-8'))

        # creating login details
        signup_details_dict = {'id': 1, 'name': 'thomas' , 'username': 'thomas', 'birthdate': datetime.datetime(2025,10,25),'image': 'sir', 'sex': 'M','location': 'here',
                         'nationality':None, 'height': None, 'religion' :None}

        # sending login details
        signup_details = json.dumps(signup_details_dict)
        self_socket.send(signup_details.encode('utf-8'))

# client.listen(1)
# while True:
#     server, address = client.accept()
#     if server !=None:
#         print(server)
#         print(address)
#         break
