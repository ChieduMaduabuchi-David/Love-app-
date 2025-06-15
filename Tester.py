# import pytz
# import datetime
# from pytz import timezone
# todaysdate = datetime.datetime.now(timezone('Europe/Warsaw'))
from Userclasses import  *
from Database import *
#.astimezone(pytz.timezone('Europe/Warsaw')))





user1 = User(
    id=1,
    name="Alice Smith",
    username="asmith",
    birthdate=datetime.datetime(1997, 6, 14),
    photo=None,
    sex="FEMALE",
    location="Berlin",
    nationality="German",
    height=height(165),
    religion="Christianity",
    interest=["hiking", "traveling"],
    intro="Adventurous and curious."
)
user1.default_desire()

user2 = User(
    id=2,
    name="Bob Johnson",
    username="bobbyj",
    birthdate=datetime.datetime(1990, 3, 10),
    photo=None,
    sex="MALE",
    location="Warsaw",
    nationality="Polish",
    height=height(180),
    religion="Agnostic",
    interest=["coding", "chess"],
    intro="Quiet thinker who loves puzzles.",
    desire=Desire(
        age=30,
        photo=None,
        sex="FEMALE",
        location="Warsaw",
        nationality="Polish",
        height=height(170),
        intro="Someone who loves logic."
    )
)

user3 = User(
    id=3,
    name="Carlos Diaz",
    username="cdiaz",
    birthdate=datetime.datetime(1985, 12, 5),
    photo=None,
    sex="MALE",
    location="Madrid",
    nationality="Spanish",
    height=height(175),
    religion="Catholic",
    interest=["football", "music"],
    intro="Easygoing and loyal."
)
user3.default_desire()

user4 = User(
    id=4,
    name="Diana Petrova",
    username="dpetrova",
    birthdate=datetime.datetime(1993, 11, 20),
    photo=None,
    sex="FEMALE",
    location="Sofia",
    nationality="Bulgarian",
    height=height(160),
    religion="Orthodox",
    interest=["dancing", "photography"],
    intro="Creative spirit.",
    desire=Desire(
        age=33,
        photo=None,
        sex="MALE",
        location="Sofia",
        nationality="Bulgarian",
        height=height(180),
        intro="Must love the arts."
    )
)

user5 = User(
    id=5,
    name="Ethan Lee",
    username="elee",
    birthdate=datetime.datetime(2001, 1, 25),
    photo=None,
    sex="MALE",
    location="London",
    nationality="British",
    height=height(178),
    religion=None,
    interest=["gaming", "reading"],
    intro="Looking for deep conversations."
)
user5.default_desire()



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
