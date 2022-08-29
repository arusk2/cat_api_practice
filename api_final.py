from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from mongoengine import connect, Document, StringField, IntField
import Calculator

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}


class CalculatorAdd(Resource):
    def post(self):
        req = request.get_json()
        # Printing our request. we can see its format is a {'first':2, 'second':2}
        print(req)
        first = req['first']
        second = req['second']

        calc = Calculator.Calculator()
        result = calc.add(first, second)
        return result, 200 #200 is the OK code


class CalculatorSubtract(Resource):
    def post(self):
        req = request.get_json()
        first = req['first']
        second = req['second']

        calc = Calculator.Calculator()
        return calc.subtract(first, second), 200

"""
When working with Databases, we have several common operations: Create, Read, Update, Delete (Or CRUD)
A RESTful API is a great way to implement these. We're using a MongoDB as our database option, 
which is referred to as an "object storage" database as it stores items without a preset Schema, unlike a relational 
database like MySQL. However, since we're working with this programmatically, we'll be using mongoengine to help
give us a schema, much like a class instance. This will help us!

First we must establish some globals we'll be using.
"""
USER = 'cat-db-user'
PASS = ''  # This is bad practice don't do this in prod
DB = 'cat-test'
MONGO_URI = f"mongodb+srv://{USER}:{PASS}@cluster0.sqqpzjf.mongodb.net/?retryWrites=true&w=majority"

# Now lets define a function to connect us to this database. This allows for database to be passed in as a string arg.
# If we are pulling from multiple databases,
def db_connect(database):
    db_uri = MONGO_URI
    db = connect(database, host=db_uri)
    return db

"""
format: db = db_connect(DB)
        db.close()

# Notes for Self
# defining page, Which is where we store items. All items with this class, Cat, 
# will save on the same page in Mongo DB, "Cat":
class Cat(Document):
    name = StringField(max_length=100, required=True)
    age = IntField()
    major = StringField(max_length=100)


Adding new items: var = PageName(field1='', field2='', fieldx='') 
where PageName is the defined page as given. (in our cast, its Cat.) and each value in args matches type.
then: var.save()
"""

"""
We want to be able to do CRUD operations to the database. (Create, Read, Update, Delete). These are done with
our REST API. why?
We don't want to transfer the entire contents of the database to our code to add an entry, or to read entries.
That's hugely wasteful. Instead, we want to only data that the database (for updating) or the user (for reading) needs.
This is our "State" (the S in Rest). As the client, we are using only a "REpresentation" of the changes in the "State" and only
"Transferring" that to the server.. (RE S T... see?)

In order to add data in a flexible but consistent form, we will make a class that inherets Document from Mongoengine. 
Using this will also make sure all data is saved to the Cat page on the MongoDB server, so that this API only interfaces 
with that page. If we had other resources, we could also connect those with separate classes.
"""

class Cat(Document):
    name = StringField(max_length=100, required=True)
    age = IntField()
    major = StringField(max_length=100)


class AddCat(Resource):
    def post(self):
        # Parse the body of the request. Request should include Name, age and major
        req = request.get_json()
        name = req['name']
        age = req['age']
        major = req['major']

        # Using Mongo Engine, we can create a Cat object. This can then be saved to the active DB
        # we will connect to the DB with each API RIGHT NOW only as a security measure.
        # This could be improved, especially if we have high traffic on the site.
        db = db_connect(DB)  # DB is our global variable for the specific page name.
        new_cat = Cat(name=name, age=age, major=major)
        new_cat.save()
        db.close()

        # Here we would decide what to return. Since this is a toy case, we will always return 200.
        # Improvements: If auth fails, we return some other HTML code? what about if the record exists already?
        return 200



# adding resource name and the path to find the resource
api.add_resource(HelloWorld, '/')
api.add_resource(CalculatorAdd, '/add', methods=['POST'])
api.add_resource(CalculatorSubtract, '/subtract', methods=['POST'])
api.add_resource(AddCat, '/newcat', methods=['POST'])

if __name__ == '__main__':
    app.run()