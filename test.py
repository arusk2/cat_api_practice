"""
This file contains scripts used both for testing and illustrating how we can use API calls.
We can pretend this file is a front end of a site, it makes async calls to our api, and when
the api calls return with data, we then put that in our website
Except here, we will be printing all of this to a console.

The flask server will need to be running to execute these. A check is made in each script.
"""
import json
import sys
import requests
URL = 'http://127.0.0.1:5000/' #127.0.0.1 is local host, 5000 is default port

def check_server() -> bool:
    # This checks that a local server is running on the default port localhost:5000.
    # If wanting to use another port, change the url variable
    get = requests.get(URL)
    if get.status_code != 200:
        print("Server is not running. To run, use command:")
        print("flask --app api.py --debug run")
        return False
    return True

def test_calculator():
    if check_server() is True:
        usr_input = ''
        print("Uses:")
        print("\t'add <number> <number>' to test the addition API call")
        print("\t'subtract <number> <number>' to test the subtraction API call")
        print("\t'exit' to exit")
        while usr_input != 'exit':
            usr_input = input()
            inp = usr_input.split(' ')
            if inp[0] == 'add' or inp[0] == 'subtract':
                url = URL + inp[0]
                resp = requests.post(url, json={'first': int(inp[1]), 'second': int(inp[2])})
                if resp.status_code == 200:
                    result = resp.text.strip('\n')  # resp.text is formatted as a new line-terminated string
                    result = int(result)
                    if inp[0] == 'add':
                        sign = "+"
                    else:
                        sign = "-"
                    print(f"Status Code: {resp.status_code} \t {inp[1]} {sign} {inp[2]} = {result}")
                else:
                    print(f"API Error, Status Code: {resp.status_code}")
        print("Exiting testing.")


def test_database():
    print("Testing db will imp later")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'c':
            test_calculator()
        elif sys.argv[1] == 'd':
            test_database()
        else:
            print("Please use 'c' to test calculator API or 'd' to test Database API.")
    else:
        print("Please use 'c' to test calculator API or 'd' to test Database API.")
        print("Format: 'python test.py <letter>'")