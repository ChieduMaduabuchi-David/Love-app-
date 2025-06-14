import datetime
import pytz
from pytz import timezone



class height:
    def __init__ (self, distance:float):
        self.cm=distance
        self.feet=distance*0.0328084

    def __repr__(self):
        return f"{self.cm} cm ({self.feet:.2f} ft)"

class Desire:
    def __init__(self, age: int, photo, sex: str, location: str, nationality: str, height: height, intro: str):
        self.age = age
        self.photo = photo
        self.sex = sex
        self.location = location
        self.nationality = nationality
        self.height = height
        self.intro = intro

    def __repr__(self):
        return (f"Desire(age={self.age}, photo={self.photo}, sex='{self.sex}', "
                f"location='{self.location}', nationality='{self.nationality}', "
                f"height={self.height}, intro='{self.intro}')")

# class of a user
class User:
    def __init__(self, id: int, name: str, username: str, birthdate: datetime.datetime,photo: None, sex: str,location: str,
                 nationality = None, height: height = None, religion: str = None, interest: list = None, intro: str= None, desire: Desire =None):
        self.id = id
        self.name = name
        self.u_name= username
        self.birthdate = birthdate
        self.photo = photo
        self.sex = sex
        self.location = location
        self.nationality = nationality
        self.height = height
        self.religion =religion
        self.interest =interest
        self.intro = intro
        self.desire = desire


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
        sex: {self.sex}.
        location {self.location}. 
        nationality {self.nationality}.
        height: {self.height}.
        intro {self.intro}.'''

    def __repr__(self):
        return (f"user id : {self.id}.\n"
                f"Name: {self.name}.\n"
                f"username: {self.u_name}.\n"
                f"age: {self.age()}.\n"
                f"photo: {self.photo}.\n"
                f"sex: {self.sex}.\n"
                f"location {self.location}.\n"
                f"nationality {self.nationality}.\n"
                f"height: {self.height}.\n"
                f"religion: {self.religion}.\n"
                f"interest: {', '.join(self.interest)}.\n"
                f"intro: {self.intro}.\n"
                "Desire: "+str(self.desire)+"\n")

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