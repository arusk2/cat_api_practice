from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
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




# adding resource name and the path to find the resource
api.add_resource(HelloWorld, '/')
api.add_resource(CalculatorAdd, '/add', methods=['POST'])
api.add_resource(CalculatorSubtract, '/subtract', methods=['POST'])

if __name__ == '__main__':
    app.run()