from flask import Flask
from flask_restful import Resource, Api, reqparse
import Calculator

app = Flask(__name__)
api = Api(app)

# Need to create a parser for our arguments
parser = reqparse.RequestParser()
parser.add_argument('first')
parser.add_argument('second')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class CalculatorAdd(Resource):
    def get(self, first, second):
        calc = Calculator.Calculator()
        result = calc.add(first, second)
        print(result)
        return result, 200 #200 is the OK code

class CalculatorSubtract(Resource):
    def get(self, first, second):
        calc = Calculator.Calculator()
        return calc.subtract(first, second), 200

# adding resource name and the path to find the resource
api.add_resource(HelloWorld, '/')
api.add_resource(CalculatorAdd, '/add/<int:first>/<int:second>')
api.add_resource(CalculatorSubtract, '/subtract/<int:first>/<int:second>')

if __name__ == '__main__':
    app.run()