import json
from logging import exception

import firebase_admin
from firebase_admin import credentials, firestore
from pyparsing import (
    Word, alphanums, oneOf, Keyword, CaselessKeyword,
    dblQuotedString, removeQuotes, infixNotation, opAssoc, pyparsing_common
)


cred = credentials.Certificate('credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


# command line looping function
def query_loop():
    print("Mini Query Language REPL")
    print("Type queries like: make == Porsche and BHP > 1000")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        query = input("-> ").strip()

        if query.lower() == "exit" or query.lower() == "quit":
            print("Goodbye")
            break

        # skip empty lines
        if not query:
            continue

        try:
            results = parse_query(query)
            print("Parsed conditions:", results)
        except Exception as e:
            print("Error parsing query:", e)


# parsing function that takes in command line, includes help
def parse_query(query: str):
    """
        Parse a query string and return a list of (field, operator, value).
    """
    # Set up the query language
    # Keywords
    MAKE = Keyword("make")
    MODEL = Keyword("model")
    YEAR = Keyword("year")
    BHP = CaselessKeyword("BHP")  # case insensitive
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
    identifier = Word(alphanums + "_")

    value = integer | boolean | quoted_string | identifier

    # Condition
    condition = field("field") + operator("op") + value("value")


# query function to communicate with database and get data

# pretty printing function?

query_loop()

# doc_ref = db.collection("cool_cars").document("car2")
# doc = doc_ref.get()
# if doc.exists:
#     print(f"Document data: {doc.to_dict()}")
# else:
#     print("No such document!")


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


    def to_dict(self):
        doc_ref = db.collection("Cool_Cars").document(str(self))
        return doc_ref.get()

    def __repr__(self):
        return f"Car(\
                make={self.make}, \
                model={self.model}, \
                BHP={self.BHP}, \
                transmission={self.transmission}, \
                convertible={self.convertible}\
            )"

