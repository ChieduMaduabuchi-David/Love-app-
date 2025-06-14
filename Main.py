import datetime
import json
import threading
import socket
import pytz
from pytz import timezone



class height:
    def __init__ (self, distance:float):
        self.cm=distance
        self.feet=distance*0.0328084


# class of a user
class User:
    def __init__(self, id: int, name: str, username: str, birthdate: datetime.datetime,photo: None, sex: str,location: str,
                 nationality = None, height: height = None, religion: str = None, intro: str= None, desire: User =None):
        self.id = id
        self.name = name
        self.u_name= username
        self.birthdate = birthdate
        self.photo = photo
        self.sex = sex
        self.location = location
        self.nationality = nationality
        self.height = height
        self.intro = intro
        self.desire = Desire


    def age(self):
        '''this has to be edited to take geolocation data from client'''
        todaysdate = datetime.datetime.now(timezone('Europe/Warsaw'))
        age = todaysdate.year - pytz.utc.localize(self.birthdate).year
        #acconts for the difference in months
        if (todaysdate.month, todaysdate.day) < (self.birthdate.month, self.birthdate.day):
            age -= 1
        return age

    def text(self):
        return f''' user id : {self.id}.
        Name: {self.name}.
        username: {self.u_name}.
        age: {self.age()}.
        photo: {self.photo}. 
        sex: {self.sex}.
        location {self.location}. 
        nationality {self.nationality}.
        height: {self.height}.
        intro {self.intro}.
        Desire {self.desire} '''



    def message(self):
        pass

    def search(self):
        pass


class Preminum_User (User):
    def __init__(self, id: int, name: str, username: str, birthdate: datetime.datetime,image: str, sex: str,location: str,
                 nationality = None, height = None, religion = None):
        super().__init__(id, name, username, birthdate, image, sex,location)
        self.religion = religion

    def message(self):
        pass

    def search(self):
        pass
        #It will have some kind of pass_port mode

    def profile_view(self):
        pass

    def first_text(self):
        #will allow user to text first
        pass

    def Hide_age(self):
        pass






























































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

