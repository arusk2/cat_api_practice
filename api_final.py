from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from mongoengine import connect
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
PASS = '###########'  # This is bad practice don't do this in prod
DB = 'cat-test'
MONGO_URI = f"mongodb+srv://{USER}:{PASS}@cluster0.sqqpzjf.mongodb.net/?retryWrites=true&w=majority"
# Now lets define a function to connect us to this database. This allows for database to be passed in a string arg.
def db_connect(database):
    db_uri = MONGO_URI
    db = connect(database, host=db_uri)
    return db

"""
format: db = db_connect(DB)
        db.close()

defining page:
class Cat(Document):
    name = StringField(max_length=100, required=True)
    age = IntField()
    major = StringField(max_length=100)


Adding new items: var = PageName(field1='', field2='', fieldx='') 
where PageName is the defined page as given. (in our cast, its Cat.) and each value in args matches type.
then: var.save()
"""


# adding resource name and the path to find the resource
api.add_resource(HelloWorld, '/')
api.add_resource(CalculatorAdd, '/add', methods=['POST'])
api.add_resource(CalculatorSubtract, '/subtract', methods=['POST'])

if __name__ == '__main__':
    app.run()