import json

import os
import mongoengine
from flask import Flask, request
from flask_restful import Resource, Api
from mongoengine import connect, Document, StringField, IntField
from mongoengine.connection import disconnect
from Calculator import Calculator

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}


class CalculatorAdd(Resource):
    # POST Methods have a body that can contain the variables needed for the function call. We can establish them in our
    # Documentation to make sure we keep a uniform interface.
    # For this API, we have two variables, 'first' and 'second', which can be accessed like any key in a python
    # dictionary once we parse the json of the request.
    def post(self):
        # First, we must parse the Body of the POST (converting JSON to something Python read-able

        # Second, lets save those two variables we know we should have.
        # What happens if the client doesn't include this or misspells it? How can we improve the security of this?

        # Third, we need to connect our API to the resource.
        # In this case, we'll be creating an object of class Calculator. We've imported it at the top

        # Fourth, once we've connected to the resource, we must tell it what we want it to do
        result = 0 # change this to a function call.
        # Fifth return result to client and return an HTTP status code.
        return result, 200 #200 is the OK code


class CalculatorSubtract(Resource):
    def post(self):
        # First, we must parse the Body of the POST (converting JSON to something Python read-able

        # Second, lets save those two variables we know we should have.
        # What happens if the client doesn't include this or misspells it? How can we improve the security of this?

        # Third, we need to connect our API to the resource.
        # In this case, we'll be creating an object of class Calculator. We've imported it at the top

        # Fourth, once we've connected to the resource, we must tell it what we want it to do
        result = 0 # change this to a function call.
        # Fifth return result to client and return an HTTP status code.
        return result, 200

# Now that we have intended functionality in our API, we need to add that functionality as
# a resource to flask's API class that we created above. This includes the Class name and the path
# to find the resource and the methods by which we want the class to be accessed. When a request is received to
# the path, with the type GET, the API will look to the HelloWorld class to see if it has a GET method implemented
# This is why above we have the CalculatorMethod as a class but the actual functionality of the class
# under method with the generic name "post", because we are saying
# "use the post method in the calculator class when we receive a post request to this specific path"
api.add_resource(HelloWorld, '/', methods=['GET'])
# Following this model, lets add our two calculator paths with the paths being '/add' and '/subtract'

"""
When working with Databases, we have several common operations: Create, Read, Update, Delete (Or CRUD)
A RESTful API is a great way to implement these. We're using a MongoDB as our database option, 
which is referred to as an "object storage" database as it stores items without a preset Schema, unlike a relational 
database like MySQL. However, since we're working with this data programmatically and have a uniform interface with 
our API, we'll be using mongoengine to help give us a schema, much like a class instance. 
First we must establish some globals we'll be using.
"""
USER = 'cat-db-user'
PASS = os.getenv('DB_PASS')  # Read the DB_PASS variable's contents into the variable, so the password is only typed in the terminal, not in the public source code. If you also need to secure against "people who can read my terminal history", call a professional.
DB = 'cat-test'
# URI Provided by Mongo DB
MONGO_URI = f"mongodb+srv://{USER}:{PASS}@cluster0.sqqpzjf.mongodb.net/?retryWrites=true&w=majority"

"""In order to add data in a flexible but consistent form, we will make a class that inherits Document from Mongoengine. 
Using this will also make sure all data is saved to the Cat page on the MongoDB server, so that this API only interfaces 
with that page. If we had other resources, we could also connect those with separate classes."""

class Cat(Document):
    name = StringField(max_length=100, required=True)
    age = IntField()
    major = StringField(max_length=100)

""" Notes for about MongoEngine (This is an implementation specific to mongoengine
we need to define a page, Which is where we store items with mongoengine
All items with this class, Cat, will save on the same page in Mongo DB, "Cat"
It must inherent the mongoengine class Document
StringField and IntField are requirements by MongoEngine so we can store data effectively in the db

Adding new items: var = PageName(field1='', field2='', fieldx='') 
where PageName is the defined page as given. (in our case, its Cat) and each value in args matches type.
We simply create a Cat object by saying: new_cat = Cat(name='', age='', major=''), just like we'd create a class object 
normally. This adds a new entry to the 'Cat' Page on the database at the MongoDB URI we've previously established.
Saving the data:
    var.save() 
"""

""" We want to be able to do CRUD operations to the database. (Create, Read, Update, Delete). These are done with
our REST API. why?
We don't want to transfer the entire contents of the database to our code to add an entry, or to read entries.
That's hugely wasteful. Instead, we want to include only data that the database needs to use (for updating) 
or the user needs (for reading). This is our "State" (the S in REST). The state is usually a subset of database, 
and is treated as a "REpresentation" of database itself. We then make changes to the "State" and "Transfer" it back 
that to the server. (RE S T... see?)
Example: The Create Operation: The State starts empty, because the new entry doesn't exist in our 
    Representation of the DB. Then, we modify the State to have a new record, Transfer that back to the original
    Representation & the DB handles adding that record into its larger pieces.
"""

# Create
class AddCat(Resource):
    def post(self):
        # First Parse the body of the request so that the JSON is read-able by python

        # Second, grab the variables from the body of the request. Here we should be given variables called 'name
        # 'age' and 'major'. For now, we will assume the client will always pass valid values for all three, but
        # an improvement would be doing validation that age is a number, none of these fields are null, etc


        # Third, we must connect to our resource, the DB. We're utilizing globals established above for convenience.
        # This is done for you here, but in the RUD ops I will leave it blank for you to add.
        # (Hint: we always connect the same way)
        connect(alias=DB, host=MONGO_URI)
        # Fourth, Using Mongo Engine, we can create a Cat object. This can then be saved to the database we
        # connected to above. This technically returns a database object, but we are not using it, so we won't
        # save it. Once the connection is established, we can create the Cat Object and use the Cat.save()
        # function saves the new object to the database we connected to with DB

        # Fifth, we need to disconnect from the database once this call is done. I think its good practice to always
        # connect and disconnect in the API call so that you know you're handling your connections and once the
        # API call is done there aren't hanging connections needing to be closed.
        # Again, this is done for you here but will need to be implemented in later RUD ops (same hint applies)
        disconnect(alias=DB)

        # Here we would decide what to return. Since this is a toy case, we will always return 200. We don't want
        # to return any data from the database.
        # Improvements: If auth fails, should we return some other HTML code?
        # What about if the record exists already or the user doesn't use the correct fields?
        return 200


# Read
class FindCatByNick(Resource):
    def post(self):
        # First Parse the body of the request so that the JSON is read-able by python

        # Second, grab the variables from the body of the request. This API only supports searching by Name, so the
        # only variable should be 'name'. let's save it as a variable called 'find'
        find = ''

        # Third, connect to DB (See previous function)

        # Fourth, Because we are searching a database, we need to be ready to catch exceptions. Mongoengine will throw
        # an exception if the record we are trying to find doesn't exist in the DB. This is more about the specifics of
        # Mongoengine, so I'm leaving this code in as "complete" just with examples.
        try:
            ret = Cat.objects.get(name=find)  # This returns a QuerySet obj that we need to convert to JSON
            # we convert to json because that is the language that we are transferring data into and out of the API
            ret = ret.to_json()
        except mongoengine.DoesNotExist:
            # There are two errors possible for Cat.objects.get(), so we need to catch and handle both.
            # If it doesn't exist, we have nothing to return
            ret = None
        except mongoengine.MultipleObjectsReturned:
            # The second error is if multiple are returned. This here is a trivial solution: we just return the first
            # This could be improved or iterated upon, but for the toy example it works.
            # For this, we aren't using get() (because get only returns one item or throws these two errors)
            # We are filtering for the name in the database itself and just returning the first in the list. We could
            # return a list, potentially, but the client must know this is possible, so they can handle it (this isn't
            # implemented in our client application)
            ret = Cat.objects(name=find)[0]  # return the first instance of the cat
            ret = ret.to_json()

        # Fifth, Disconnect from DB

        # Improvements: should our status code be different if the DoesNotExist exception was thrown?
        return ret, 200


# Update -- We are assuming client has full view of a resource and will pass in all available fields.
# I'd implement this client side by first calling FindCat to retrieve data and then modifying given record,
# and sending the whole record back with the previous name as a find term (Remember our database isn't actually updated
# until we second the record back with this modify function
# ModifyCat then can make the assumption that the record always exists (or FindCatByNick would have failed)
class ModifyCat(Resource):
    def post(self):
        # First Parse the body of the request so that the JSON is read-able by python

        # Second we need to pull our variables from the request. We have 'name', 'newName', 'age' and 'major'
        # Casing is important, and I mostly see camelCase in JSON (hence why I've structured it that way)
        # I've named the variables here because the names are used in code below, replace the Nones
        find = None
        new_name = None
        new_age = None
        new_major = None
        # Third, Connect to DB

        # Fourth, We are searching the database for the record we want to update. Why? we want the unique ID that the
        # DB assigns to every entry so we can be sure we're updating the right one. This is already done in the Read
        # function (which we assume was used first to get the record) so this is an area of improvement. How would you
        # Modify this so that we are getting the ID of the record in the request?
        try:
            update = Cat.objects.get(name=find)
        except mongoengine.MultipleObjectsReturned:
            # We can assume it exists because of the read, but there still might be multiple, so we grab the first.
            # If we don't handle this exception it causes the API to crash
            update = Cat.objects(name=find)[0]
        finally:
            # This will always happen after either the try or except block execute. We are updating the entry using the
            # ID provided for better accuracy. We are updating all fields, even if only one is changed.
            Cat.objects(id=update.id).update(name=new_name, age=new_age, major=new_major)

        # Fifth, disconnect

        # This is probably the most rudimentary function and could be improved. What are some ways we improve it?
        return 200


# Delete Cat
# returns 200 if cat entry was deleted, returns 400 if cat does not exist
# How can we improve this? what can we use that's more specific than a name?
class DeleteCat(Resource):
    def post(self):
        # First Parse the body of the request so that the JSON is read-able by python

        # Second, let's get the only required variable passed in by the request body, 'name'
        find = None
        # Third, Connect to DB

        # Fourth, we are trying to get the record we want to delete. This way we can access its ID, similar to Update.
        # then, we delete it if it exists. If it doesn't exist, we send back an error code and an error message.
        # Because this is a specific implementation of mongoengine, I included the code. The *pattern* will be the same
        # with any DB but the *syntax* will vary. our focus is on *patterns*
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
        ret_msg = json.dumps(ret_msg)  # we need to convert this to JSON to pass through API
        # Fifth, disconnect

        # Now, we have two things to return, the message and the code. Message goes first, then code.
        # Once we improve the update function, is there a way we can improve this functionality? It should be noted I
        # didn't make the assumption that a read was called before the delete call, so in our documentation maybe we can
        # establish a precedent: do update and delete call read themselves or is it on the client? how does this change
        # how we use return codes or return messages? These idiosyncrasies are easy to plan for when we're client, API
        # writer and resource manager, but if we're only one of those we need to iron them out.
        return ret_msg, ret_stat


# FINALLY we've established a BUNCH of functionality, but we need to make sure the API knows what it should call based
# on the path of the request and type its given. We will structure this similarly to the Calculator, with the name of
# the class first, then the path we find it at, then the methods accepted. For this, all methods are POST, and paths are:
# Create: /newcat
# Read: /findcat
# Update: /modifycat
# Delete: /deletecat

# This will run our webserver until we quit with CTRL+C
if __name__ == '__main__':
    app.run()