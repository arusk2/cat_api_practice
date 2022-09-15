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