import json
import firebase_admin
from firebase_admin import credentials, firestore
import pyparsing


cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


# command line looping function

# parsing function that takes in command line, includes help

# query function to communicate with database and get data

# pretty printing function?

doc_ref = db.collection("cool_cars").document("car2")
doc = doc_ref.get()
if doc.exists:
    print(f"Document data: {doc.to_dict()}")
else:
    print("No such document!")


# Class Cool_Car
class Cool_Car:
    def __init__(self, make, model, year, BHP, transmission, convertible=False):
        self.make = make
        self.model = model
        self.year = year
        self.BHP = BHP
        self.transmission = transmission
        self.convertible = convertible

    @staticmethod
    def from_dict(source):
        #d

    def to_dict(self):
        # ...

    def __repr__(self):
        return f"Car(\
                make={self.make}, \
                model={self.model}, \
                BHP={self.BHP}, \
                transmission={self.transmission}, \
                convertible={self.convertible}\
            )"

