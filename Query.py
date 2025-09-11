import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import FieldFilter
from pyparsing import (
    Word, alphanums, oneOf, Keyword, CaselessKeyword,
    dblQuotedString, removeQuotes, infixNotation, opAssoc, pyparsing_common
)


cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
collection = "cool_cars"

# command line looping function
def query_loop():
    print("Mini Query Language")
    print("Type queries like: make == Porsche and BHP > 1000")
    print("model == \"Ford Mustang\"")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("-> ").strip()

        if query.lower() == "exit" or query.lower() == "quit":
            print("Goodbye")
            break
        elif query.lower() == "help":
            print("Mini Query Language")
            print("Type queries like: make == Porsche and BHP > 1000")
            print("model == \"Ford Mustang\"")
            print("Type 'exit' or 'quit' to stop.\n")


        # skip empty lines
        if not query:
            continue

        if query.lower() != "help":
            try:
                results = parse_query(query.lower())
                print("Parsed conditions:", query_to_Firebase(results))
            except Exception as e:
                print("Error parsing query:", e)


# parsing function that takes in command line string, includes help
def parse_query(query: str):
    # Keywords
    MAKE = Keyword("make")
    MODEL = Keyword("model")
    YEAR = Keyword("year")
    BHP = CaselessKeyword("BHP")
    TRANSMISSION = Keyword("transmission")
    CONVERTIBLE = Keyword("convertible")
    HELP = Keyword("help")

    field = MAKE | MODEL | YEAR | BHP | TRANSMISSION | CONVERTIBLE | HELP

    # Operators
    operator = oneOf("== != < <= > >=")

    # Values
    integer = pyparsing_common.integer
    boolean = oneOf("True False").setParseAction(lambda t: t[0] == "True")
    quoted_string = dblQuotedString.setParseAction(removeQuotes)

    # Exclude reserved words
    reserved = {"and", "or", "True", "False"}
    identifier = Word(alphanums + "_").setParseAction(
        lambda t: t[0] if t[0] not in reserved else None
    )

    value = integer | boolean | quoted_string | identifier

    # Single condition
    condition = (field + operator + value).setParseAction(lambda t: (t[0], t[1], t[2]))

    # Boolean logic (force and/or as operators here)
    expr = infixNotation(
        condition,
        [
            (CaselessKeyword("and"), 2, opAssoc.LEFT),
            (CaselessKeyword("or"), 2, opAssoc.LEFT),
        ]
    )

    # Parse
    parsed = expr.parseString(query, parseAll=True)
    tree = parsed.asList()[0]
    return tree


def query_to_Firebase(query):

    response = db.collection(collection).where(filter=FieldFilter('model','==','i8')).stream()
    for doc in response:
        print(f"{doc.id} => {doc.to_dict()}")

# query function to communicate with database and get data

# doc_ref = db.collection("cool_cars").document("car2")
# doc = doc_ref.get()
# if doc.exists:
#     print(f"Document data: {doc.to_dict()}")
# else:
#     print("No such document!")

# pretty printing function?

query_loop()


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
        cars = db.collection(collection).stream()
        new_car_number = len(cars) + 1
        db.collection(collection).document(f"car{new_car_number}").set(source)


    def to_dict(self):
        doc_ref = db.collection(collection).document(str(self))
        return doc_ref.get()

    def __repr__(self):
        return f"Car(\
                make={self.make}, \
                model={self.model}, \
                BHP={self.BHP}, \
                transmission={self.transmission}, \
                convertible={self.convertible}\
            )"

    def print(self):
        result = ""
        result += self.year + " " + self.make + " " + self.model
        if(self.convertible):
            result += " convertible\n"
        result += self.transmission + " transmission with " + self.BHP + " horsepower."
        print(result)

