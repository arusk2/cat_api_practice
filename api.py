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
    # Following this model, lets add our two calculator paths with the path being '/add' and '/subtract'

    """
    When working with Databases, we have several common operations: Create, Read, Update, Delete (Or CRUD)
    A RESTful API is a great way to implement these. We're using a MongoDB as our database option, 
    which is referred to as an "object storage" database as it stores items without a preset Schema, unlike a relational 
    database like MySQL. However, since we're working with this data programmatically and have a uniform interface with 
    our API, we'll be using mongoengine to help give us a schema, much like a class instance. 
    First we must establish some globals we'll be using.
    """
    USER = 'cat-db-user'
    PASS = ''  # This is bad practice don't do this in prod. This should be somewhere secret not saved to the repo
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

            # Fifth, we need to disconnect from the database once this call is done. I think its goo practice to always
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
        req = request.get_json()
        find = req['name']

        connect(alias=DB, host=MONGO_URI)
        try:
            ret = Cat.objects.get(name=find)  # This returns a QuerySet obj that we need to convert to JSON
            ret = ret.to_json()
        except mongoengine.DoesNotExist:
            ret = None
        except mongoengine.MultipleObjectsReturned:
            ret = Cat.objects(name=find)[0]  # return the first instance of the cat
            ret = ret.to_json()
        disconnect(alias=DB)
        return ret, 200
