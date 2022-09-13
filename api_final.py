import mongoengine
from flask import Flask, request
from flask_restful import Resource, Api
from mongoengine import connect, Document, StringField, IntField
from mongoengine.connection import disconnect
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

# adding resource name and the path to find the resource. This gives the API a function to call when a request
# is received with the path AND HTTP method (GET, POST, etc)
# This is why above we have the CalculatorMethod as a class but the actual functionality under method with the generic
# name "post", because we are saying "use the post method in the calculator class when we receive a post request to this
# specific path"
api.add_resource(HelloWorld, '/')
api.add_resource(CalculatorAdd, '/add', methods=['POST'])
api.add_resource(CalculatorSubtract, '/subtract', methods=['POST'])

"""
When working with Databases, we have several common operations: Create, Read, Update, Delete (Or CRUD)
A RESTful API is a great way to implement these. We're using a MongoDB as our database option, 
which is referred to as an "object storage" database as it stores items without a preset Schema, unlike a relational 
database like MySQL. However, since we're working with this programmatically, we'll be using mongoengine to help
give us a schema, much like a class instance. This will help us!

First we must establish some globals we'll be using.
"""
USER = 'cat-db-user'
PASS = ''  # This is bad practice don't do this in prod. This should be somewhere secret not saved to the repo
DB = 'cat-test'
# URI Provided by Mongo DB
MONGO_URI = f"mongodb+srv://{USER}:{PASS}@cluster0.sqqpzjf.mongodb.net/?retryWrites=true&w=majority"

# Now lets define a function to connect us to this database. This allows for database to be passed in as a string arg.
# If we are pulling from multiple databases,
def dbConnect(database):
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


# Create
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
        db = dbConnect(DB)  # DB is our global variable for the specific page name.
        new_cat = Cat(name=name, age=age, major=major)
        new_cat.save()
        disconnect(alias=DB)

        # Here we would decide what to return. Since this is a toy case, we will always return 200.
        # Improvements: If auth fails, we return some other HTML code? what about if the record exists already?
        return 200


# Read
class FindCatByNick(Resource):
    def post(self):
        req = request.get_json()
        find = req['name']

        db = dbConnect(DB)
        try:
            ret = Cat.objects.get(name=find)  # This returns a QuerySet obj that we need to conver to JSON
            ret = ret.to_json()
        except mongoengine.DoesNotExist:
            ret = None
        except mongoengine.MultipleObjectsReturned:
            ret = Cat.objects(name=find)[0]  # return the first instance of the cat
            ret = ret.to_json()
        db.close()
        return ret, 200


# Update -- We are assuming client has full view of a resource and will pass in all available fields.
# I'd implement this client side by first calling find to retrieve data and then modifying that, and sending the
# whole record back.
# ModifyCat then can make the assumption that the record always exists (or FindCatByNick would have failed)
class ModifyCat(Resource):
    def post(self):
        req = request.get_json()
        find = req['name']
        new_name = req['newName']
        new_age = req['age']
        new_major = req['major']
        db = dbConnect(DB)
        try:
            update = Cat.objects.get(name=find)
        except mongoengine.MultipleobjectsReturned:
            update = Cat.objects(name=find)[0]
        finally:
            Cat.objects(id=update.id).update(name=new_name, age=new_age, major=new_major)
        db.close()
        return 200


# Delete Cat
# returns 200 if cat entry was deleted, returns 400 if cat does not exist
# How can we improve this? what can we use that's more specific than a name?
class DeleteCat(Resource):
    def post(self):
        req = request.get_json()
        find = req['name']
        db = dbConnect(DB)
        to_delete = None
        try:
            to_delete = Cat.objects.get(name=find)
        except mongoengine.DoesNotExist:
            to_delete = None
        except mongoengine.MultipleObjectsReturned:
            to_delete = Cat.objects(name=find)[0]  # delete the first instance of the cat
        finally:
            if to_delete is not None:
                Cat.objects(id=to_delete.id).delete()  # deleting by unique ID just in case dup names exist
                ret_msg = {"Body": "Object Deleted"}
                ret_stat = 200
            else:
                ret_msg = {"Body": f"{find} not in table"}
                ret_stat = 400  # send a bad request error.
        db.close()
        return ret_msg, ret_stat



api.add_resource(AddCat, '/newcat', methods=['POST'])
api.add_resource(FindCatByNick, '/findcat', methods=['POST'])
api.add_resource(ModifyCat, '/modifycat', methods=['POST'])
api.add_resource(DeleteCat, '/deletecat', methods=['POST'])

if __name__ == '__main__':
    app.run()