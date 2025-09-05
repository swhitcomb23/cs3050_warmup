import json
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


# command line looping function

# parsing function that takes in command line

# query function to communicate with database and get data

# pretty printing function?

doc_ref = db.collection("cool_cars").document("car2")

doc = doc_ref.get()
if doc.exists:
    print(f"Document data: {doc.to_dict()}")
else:
    print("No such document!")