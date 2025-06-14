# import pytz
# import datetime
# from pytz import timezone
# todaysdate = datetime.datetime.now(timezone('Europe/Warsaw'))
from Userclasses import  *
from Database import *
#.astimezone(pytz.timezone('Europe/Warsaw')))





user1 = User(
    id=1,
    name="Liam Garcia",
    username="liamg",
    birthdate=datetime.datetime(1993, 8, 17),
    photo=None,
    sex="male",
    location="Madrid",
    nationality="Spanish",
    height=height(178),
    religion="Atheist",
    interest=["football", "guitar", "travel"],
    intro="Easygoing guy who loves live music and road trips.",
    desire=Desire(
        age=25,
        photo=None,
        sex="female",
        location="Barcelona",
        nationality="Spanish",
        height=height(165),
        intro="Looking for someone spontaneous and adventurous.")
)


user2 = User(
    id=2,
    name="Aisha Khan",
    username="aishak",
    birthdate=datetime.datetime(1997, 5, 12),
    photo=None,
    sex="female",
    location="Dubai",
    nationality="Emirati",
    height=height(160),
    religion="Muslim",
    interest=["fashion", "calligraphy", "movies"],
    intro="A creative soul who enjoys deep conversations.",
    desire=Desire(
        age=30,
        photo=None,
        sex="male",
        location="Abu Dhabi",
        nationality="Emirati",
        height=height(180),
        intro="Seeking someone mature with a sense of humor.")
)


user3 = User(
    id=3,
    name="Noah Schmidt",
    username="noah_s",
    birthdate=datetime.datetime(1990, 11, 3),
    photo=None,
    sex="male",
    location="Munich",
    nationality="German",
    height=height(182),
    religion="Christian",
    interest=["cycling", "photography", "board games"],
    intro="Nature enthusiast and amateur photographer.",
    desire=Desire(
        age=28,
        photo=None,
        sex="female",
        location="Berlin",
        nationality="German",
        height=height(170),
        intro="Someone who loves the outdoors and art.")
)

user4 = User(
    id=4,
    name="Mei Lin",
    username="meilin88",
    birthdate=datetime.datetime(1995, 2, 25),
    photo=None,
    sex="female",
    location="Shanghai",
    nationality="Chinese",
    height=height(158),
    religion="Buddhist",
    interest=["reading", "tea ceremony", "yoga"],
    intro="Peaceful and kind-hearted, looking for real connection.",
    desire=Desire(
        age=29,
        photo=None,
        sex="male",
        location="Beijing",
        nationality="Chinese",
        height=height(175),
        intro="Wants a calm and balanced relationship.")
)

user5 = User(
    id=5,
    name="David Brown",
    username="daveb",
    birthdate=datetime.datetime(1988, 7, 1),
    photo=None,
    sex="male",
    location="Toronto",
    nationality="Canadian",
    height=height(185),
    religion="Agnostic",
    interest=["coding", "sci-fi", "dogs"],
    intro="Techie with a love for good stories and golden retrievers.",
    desire=Desire(
        age=32,
        photo=None,
        sex="female",
        location="Vancouver",
        nationality="Canadian",
        height=height(168),
        intro="A fun-loving and thoughtful partner who loves dogs.")
)
userlist = [user1, user2, user3, user4, user5]

for user in userlist:
    embed(user)






# print(todaysdate)
# # timezones = pytz.all_timezones
# # for i in timezones:
# #     print(i)
