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