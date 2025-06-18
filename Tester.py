# import pytz
# import datetime
# from pytz import timezone
# todaysdate = datetime.datetime.now(timezone('Europe/Warsaw'))
from Userclasses import  *
from Database import *
#.astimezone(pytz.timezone('Europe/Warsaw')))





users = []

names = ["Alice", "Bob", "Chloe", "David", "Eva", "Frank", "Grace", "Henry", "Isla", "Jack"]
usernames = ["alice01", "bob99", "chloe.l", "david_x", "eva_star", "frank_the_tank", "graceful", "henry_89", "isla.blue", "jack123"]
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
    datetime.datetime(1994, 9, 23)
]
sexes = ["F", "M", "F", "M", "F", "M", "F", "M", "F", "M"]
locations = ["Łódź", "Warsaw", "Kraków", "Gdańsk", "Wrocław", "Poznań", "Szczecin", "Katowice", "Lublin", "Białystok"]
emails = [f"{name.lower()}@test.com" for name in names]
phones = [f"+4812345678{i}" for i in range(10)]
photos = list(range(100, 110))
nationalities = ["Polish"] * 10
heights = [height(160 + i * 3) for i in range(10)]
religions = ["Christian", "None", "Christian", "Muslim", "Christian", "Atheist", "Christian", "Jewish", "Buddhist", "None"]
interests = [["reading", "hiking"], ["gaming", "cooking"], ["music", "travel"], ["fitness", "tech"], ["writing", "baking"],
             ["sports", "tech"], ["art", "nature"], ["movies", "cycling"], ["yoga", "volunteering"], ["coding", "chess"]]
intros = [f"Hi, I'm {name}!" for name in names]

for i in range(10):
    u = User(
        id=i+1,
        name=names[i],
        username=usernames[i],
        birthdate=birthdates[i],
        sex=sexes[i],
        location=locations[i],
        email=emails[i],
        phone=phones[i],
        photo=photos[i],
        nationality=nationalities[i],
        height=heights[i],
        religion=religions[i],
        interest=interests[i],
        intro=intros[i]
    )
    u.default_desire()
    users.append(u)




# print(eval(user5.desire))
#print(str(user5))
#print(str(user5.desire))
# print(user5.desire)
# print(repr(user5.desire))
# print(type(user5.desire))
# print(isinstance(user5.desire, Desire))


# print(user5.desire)

userlist = [user1, user2, user3, user4, user5]


'''Testing adding and searching for users'''
for user in userlist:
    embed(user)


print(search(user5))



# print(todaysdate)
# # timezones = pytz.all_timezones
# # for i in timezones:
# #     print(i)
