"""Person Class

"""


class Household(object):

    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def to_dict(self):
        return {
            'people': self.people
        }


class Person(object):

    def __init__(self, name=None, age=None, gender=None):
        self.age = age
        self.gender = gender
        self.name = name

    def to_dict(self):
        return {
            'age': self.age,
            'gender': self.gender,
            'name': self.name
        }
