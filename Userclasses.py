import datetime
import pytz
from pytz import timezone


class height:
    def __init__ (self, distance:float):
        self.cm=distance
        self.feet=distance*0.0328084

    def __repr__(self):
        return f"{self.cm} cm ({self.feet:.2f} ft)"

    def __add__(self,value):
        return self.cm + value

    def __radd__(self,value):
        return self.cm + value

    def __sub__(self, value):
        return self.cm - value

    def __rsub__(self, value):
        return self.cm - value


class Sex:
    def __init__(self,sex:str):
        sex = sex.upper().strip()
        if sex == "MALE" or sex =="M":
            sex="MALE"
        elif sex == "FEMALE" or sex=="F":
            sex = "FEMALE"
        else:
            sex = None
            raise ValueError("Only Accepts Male or Female")
        self.value = sex

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"Sex('{self.value}')"

    def flip(self):
        if self.value == "MALE":
            return "FEMALE"
        else:
            return "MALE"


class Desire:
    def __init__(self, age: int = None, photo = None, sex: str = None, location: str = None, nationality: str = None, height: height= None, intro: str = None, religion: str = None, interest: list = None):
        self.age = age
        self.photo = photo
        self.sex = Sex(sex)
        self.location = location
        self.nationality = nationality
        self.height = height
        self.intro = intro
        self.religion = religion
        self.interest = interest

    def __repr__(self):
        return (f"Desire(age={self.age}, photo={self.photo}, sex='{self.sex}', "
                f"location='{self.location}', nationality='{self.nationality}', "
                f"height={self.height}, intro='{self.intro}')")

# class of a user
class User:
    def __init__(self, id: int, name: str, username: str, birthdate: datetime.datetime, sex: str,location: str, email: str = None,phone: str = None, photo:int = None,
                 nationality = None, height: height = None, religion: str = None, interest: list = None, intro: str= None, desire: Desire =None):
        self._id = id
        self.name = name
        self.u_name= username
        self.email=email
        self.phone_number=phone
        self._birthdate = birthdate
        self.photo = photo
        self.sex = Sex(sex)
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
        age = todaysdate.year - pytz.utc.localize(self._birthdate).year
        #acconts for the difference in months
        if (todaysdate.month, todaysdate.day) < (self._birthdate.month, self._birthdate.day):
            age -= 1
        return age

    # def text(self):
    #     return f''' user id : {self.id}.
    #     Name: {self.name}.
    #     username: {self.u_name}.
    #     age: {self.age()}.
    #     sex: {self.sex}.
    #     location {self.location}.
    #     nationality {self.nationality}.
    #     height: {self.height}.
    #     intro {self.intro}.'''

    def __repr__(self):
        return (f"user id : {self._id}.\n"
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

    def default_desire(self):
        dheight=None
        if self.height != None:
            if self.sex.value == "FEMALE":
                dheight=21+self.height
            else:
                dheight=self.height-11.43

        self.desire = Desire(
            age=self.age(),
            photo=None,
            sex=self.sex.flip(),
            location=self.location,
            nationality=self.nationality,
            height=dheight,
            intro=self.intro,
            interest=self.interest
        )


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