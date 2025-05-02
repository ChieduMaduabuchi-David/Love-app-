class Person:
    def __init__(self, id: int, name: str, birthdate: int,image: str, sex: str,location: str ):
        self.id = id
        self.name = name
        self.birthdate = birthdate
        self.image = image
        self.sex = sex
        self.location = location
        self.nationality = None
        self.height = None
        self.Religion = None

    def age(self):




chiedu = Person(123, "chiedu",7252004, "hey", "M", "Poland" )
print(chiedu.name)

