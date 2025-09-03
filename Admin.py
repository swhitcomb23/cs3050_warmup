import json
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

print('works')