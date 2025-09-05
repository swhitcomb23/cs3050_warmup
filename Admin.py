import json
from pickle import FALSE

import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

with open('cool_cars.json') as f:
    data = json.load(f)

cars = data.get("cool_cars", {})
for car_id, car_info in cars.items():
    db.collection("cool_cars").document(car_id).set(car_info)


class Cool_Car:
    def __init__(self, make, model, year, BHP, transmission, convertible=FALSE):
        self.make = make
        self.model = model
        self.year = year
        self.BHP = BHP
        self.transmission = transmission
        self.convertible = convertible

    @staticmethod
    def from_dict(source):
        # ...

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

