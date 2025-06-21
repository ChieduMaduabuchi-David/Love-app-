import socket
import datetime
import pytz
import time
import json
import chromadb
from  Userclasses import *


users = []

names = ["Alice", "Bob", "Chloe", "David", "Eva", "Frank", "Grace", "Henry", "Isla", "Jack","smith"]
usernames = ["alice01", "bob99", "chloe.l", "david_x", "eva_star", "frank_the_tank", "graceful", "henry_89", "isla.blue", "jack123",10]
birthdates = [
    datetime.datetime(1995, 5, 15),
    datetime.datetime(1990, 11, 3),
    datetime.datetime(1997, 2, 28),
    datetime.datetime(1988, 7, 10),
    datetime.datetime(1993, 12, 5),
    datetime.datetime(1985, 3, 21),
    datetime.datetime(2000, 8, 19),
    datetime.datetime(1992, 1, 30),
    datetime.datetime(1998, 6, 6),
    datetime.datetime(1994, 9, 23),

]
sexes = ["F", "M", "F", "M", "F", "M", "F", "M", "F", "M","M"]
locations = ["Łódź", "Warsaw", "Kraków", "Gdańsk", "Wrocław", "Poznań", "Szczecin", "Katowice", "Lublin", "Białystok","Fake place"]
emails = [f"{name.lower()}@test.com" for name in names]
phones = [f"+4812345678{i}" for i in range(11)]
photos = list(range(100, 110))
nationalities = ["Polish"] * 11
heights = [height(160 + i * 3) for i in range(11)]
religions = ["Christian", "None", "Christian", "Muslim", "Christian", "Atheist", "Christian", "Jewish", "Buddhist", "None"]
interests = [["reading", "hiking"], ["gaming", "cooking"], ["music", "travel"], ["fitness", "tech"], ["writing", "baking"],
             ["sports", "tech"], ["art", "nature"], ["movies", "cycling"], ["yoga", "volunteering"], ["coding", "chess"],["Ninan","cars"]]
intros = [f"Hi, I'm {name}!" for name in names]

passwords = ['hDy3@kLp!29Z', 'M7x#Uv!dPz1E', 'Q2s@La9v$XoT', 'cZ8@rLfYw#Q1',
 'tB#2KmU!iYpV', 'eL3@vQmR9&zX', 'F#vT91X!mYg7', 'oWr#Z7kY$1Lt',
 'Dp4!cXtV&N9z', 'Ks@2qLy!WvM1','ILYSM']

for i in range(10):
    user = {
    'id' :  i + 1,
    'name' : names[i],
    'username' : usernames[i],
    'birthdate' : birthdates[i].strftime("%Y-%m-%d %H:%M:%S"),
    'sex' : sexes[i],
    'location' : locations[i],
    'email' : emails[i],
    'phone' : phones[i],
    'photo' : photos[i],
    'nationality' : nationalities[i],
    'height' : heights[i].cm,
    'religion' : religions[i],
    'interest' : interests[i],
    'intro' : intros[i]
    }
    users.append(user)

badUser = {
    'id': "play",
    'name': 15,
    'username': " big_boy1 chris",
    'birthdate': datetime.datetime(2005,5,9).strftime("%Y-%m-%d %H:%M:%S"),
    'sex': "M",
    'location': "bleh",
    'email': "@bleh",
    'phone': +481234567809,
    'photo': 111,
    'nationality': "nigeria",
    'height': 150,
    'religion': "budist",
    'interest': ["cars","Goats"],
    'intro': "Hehe"
}

users.append(badUser)

host = socket.gethostbyname(socket.gethostname())
port = 46830





#Username and password will be properly implemented in the client side


#cheking letting the server know the user wants to login

def test_first_interaction(opt):

    if opt == 0:
        # want to sign up
        self_socket.send('True'.encode('utf-8'))

        #creating new login details
        signup_details_dict={'Username':username,'password':password}


        # sending new login details
        signup_details = json.dumps(signup_details_dict)
        self_socket.send(signup_details.encode('utf-8'))
        print(username, "+++", password)

        # sending new user details
        print(users[10])
        signup_details = json.dumps(users[10])
        self_socket.send(signup_details.encode('utf-8'))
        print(self_socket.recv(1024).decode('utf-8'))
    else:
        # want to login
        self_socket.send('True'.encode('utf-8'))

        # creating login details
        login_details_dict = {'Username': username, 'password': password}
        login_details = json.dumps(login_details_dict)
        self_socket.send(login_details.encode('utf-8'))

        print(self_socket.recv(1024).decode('utf-8'))

# for user in users:
#     print(user)
for i in range(11):
    print(i)
    self_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            self_socket.connect((host, port))
            break
        except ConnectionRefusedError:
            continue
    message = self_socket.recv(1024).decode('utf-8')
    print(message)
    username = users[i]['username']
    password = passwords[i]
    print()
    test_first_interaction(0)
    self_socket.close()


# client.listen(1)
# while True:
#     server, address = client.accept()
#     if server !=None:
#         print(server)
#         print(address)
#         break
