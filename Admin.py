import json
import sys

import firebase_admin
from firebase_admin import credentials, firestore

#This section is for the credentials, initializing firebase, and opening the client
cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

json_file = sys.argv[1]

# This section opens the json file and loads the data
with open(json_file) as f:
    data = json.load(f)

# This section loads the cool cars into documents on the firebase database
cars = data.get("cool_cars", {})
for car_id, car_info in cars.items():
    db.collection("cool_cars").document(car_id).set(car_info)

#This is a confirmation print when it is finished
print(f"data from {json_file} uploaded to Firestore successfully!")
