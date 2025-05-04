import datetime
import json
import threading
import socket
import pytz
from pytz import timezone


# class of a user

class User:
    def __init__(self, id: int, name: str, username: str, birthdate: datetime.datetime,image: str, sex: str,location: str,
                 nationality = None, height = None, religion = None):
        self.id = id
        self.name = name
        self.u_name= username
        self.birthdate = birthdate
        self.image = image
        self.sex = sex
        self.location = location
        self.nationality = nationality
        self.height = height
        self.religion = religion

    def age(self):
        '''this has to be edited to take geolocation data from client'''
        todaysdate = datetime.datetime.now(timezone('Europe/Warsaw'))
        age = todaysdate.year - pytz.utc.localize(self.birthdate).year
        #acconts for the difference in months
        if (todaysdate.month, todaysdate.day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        return age

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

