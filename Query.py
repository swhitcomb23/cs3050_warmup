
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
        cool_car = Cool_Car(source["make"], source["model"], source["BHP"], source["transmission"], source["year"], source["convertible"])

        if "make" in source:
            cool_car.make = source["make"]

        if "model" in source:
            cool_car.model = source["model"]

        if "BHP" in source:
            cool_car.BHP = source["BHP"]

        if "transmission" in source:
            cool_car.transmission = source["transmission"]

        if "year" in source:
            cool_car.year = source["year"]

        if "convertible" in source:
            cool_car.convertible = source["convertible"]

        return cool_car


    def to_dict(self):
        dest = {"make": self.make, "model": self.model, "BHP": self.BHP, "transmission": self.transmission, "year": self.year, "convertible": self.convertible}

        if self.make:
            dest["make"] = self.make

        if self.model:
            dest["model"] = self.model

        if self.BHP:
            dest["BHP"] = self.BHP

        if self.transmission:
            dest["transmission"] = self.transmission

        if self.year:
            dest["year"] = self.year

        if self.convertible:
            dest["convertible"] = self.convertible

        return dest

    def __repr__(self):
        return f"Car(\
                make={self.make}, \
                model={self.model}, \
                BHP={self.BHP}, \
                transmission={self.transmission}, \
                convertible={self.convertible}\
            )"





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
            print("Query language is case sensitive for makes and models")
            print("Wrap multy-word makes/models in double quotes")
            print("Valid keywords: make, model, year, bph, transmission, convertible")
            print("Valid logic operators: == != < <= > >=")
            print("Type 'exit' or 'quit' to stop.\n")

        # skip empty lines
        if not query:
            continue

        if query.lower() != "help":
            try:
                results = parse_query(query)
                print("Parsed conditions:", results)
                query_to_Firebase(results)
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

    field = MAKE | MODEL | YEAR | BHP | TRANSMISSION | CONVERTIBLE

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


# query function to communicate with database and get data
def query_to_Firebase(query):
    response_list = []
    response2_list = []
    response2 = []
    if 'and' in query:
        response = db.collection(collection).where(filter=FieldFilter(query[0][0], query[0][1], query[0][2])).where(filter=FieldFilter(query[2][0], query[2][1], query[2][2])).stream()
    elif 'or' in query:
        response = (db.collection(collection)).where(filter=FieldFilter(query[0][0], query[0][1], query[0][2])).stream()
        response2 = (db.collection(collection)).where(filter=FieldFilter(query[2][0], query[2][1], query[2][2])).stream()
    else:
        response = db.collection(collection).where(filter=FieldFilter(query[0], query[1], query[2])).stream()

    for doc in response:
        car = Cool_Car.from_dict(doc.to_dict())
        response_list.append(car)
    for doc in response2:
        x = Cool_Car.from_dict(doc.to_dict())
        if x not in response_list:
            response_list.append(x)
    for doc in response_list:
        print(doc)


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
        cool_car = Cool_Car(source["make"], source["model"], source["BHP"], source["transmission"], source["year"], source["convertible"])

        if "make" in source:
            cool_car.make = source["make"]

        if "model" in source:
            cool_car.model = source["model"]

        if "BHP" in source:
            cool_car.BHP = source["BHP"]

        if "transmission" in source:
            cool_car.transmission = source["transmission"]

        if "year" in source:
            cool_car.year = source["year"]

        if "convertible" in source:
            cool_car.convertible = source["convertible"]

        return cool_car


    def to_dict(self):
        dest = {"make": self.make, "model": self.model, "BHP": self.BHP, "transmission": self.transmission, "year": self.year, "convertible": self.convertible}

        if self.make:
            dest["make"] = self.make

        if self.model:
            dest["model"] = self.model

        if self.BHP:
            dest["BHP"] = self.BHP

        if self.transmission:
            dest["transmission"] = self.transmission

        if self.year:
            dest["year"] = self.year

        if self.convertible:
            dest["convertible"] = self.convertible

        return dest

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
        if (self.convertible):
            result += " convertible\n"
        result += self.transmission + " transmission with " + self.BHP + " horsepower. \n \n"
        print(result)