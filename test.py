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
        print("python flask_start.py")
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
        return


def test_database():
    if check_server() is True:
        usr_input = ''
        print("Uses:")
        print("\t 'newcat <CatNick> <age> <major>' to test the DB API and add a new cat to DB (keep major one word or abbreviation, no spaces)")
        print("\t 'findcat <CatNick>' to test the DB API find call and retrieve information about a Cat")
        print("\t 'modifycat <CatNick> <UpdatedNick> <UpdatedAge> <UpdatedMajor>' to test DB API's Update functionality and update the DB record")
        print("\t 'deletecat <CatNick>' to test DB API's Delete function and remove a cat from the DB")
        print("\t 'exit' to exit")

        while usr_input != 'exit':
            usr_input = input()
            inp = usr_input.split(' ')
            if inp[0] == 'newcat':
                test_addcat(inp[0], inp[1], inp[2], inp[3])  # path, name, age, major (all w/ no spaces)
            elif inp[0] == 'findcat':
                test_findcat(inp[0], inp[1])  # only need path and name to test find    
            elif inp[0] == 'modifycat':
                test_updatecat(inp[0], inp[1], inp[2], inp[3], inp[4])
            elif inp[0] == 'deletecat':
                test_deletecat(inp[0], inp[1])
            else:
                if not 'exit':
                    print("Make sure your input doesn't have typos")
        print("Exiting testing.")
        return

def test_addcat(path, name, age, major):
    url = URL + path
    req_body = {'name': name,
                'age': int(age),
                'major': major}  #we got the age from a string so we convert to int
    resp = requests.post(url, json=req_body)
    if resp.status_code == 200:
        print(f"New record created: \n\tNick: \t{name}\n\tAge: \t{age}\n\tMajor: \t{major}")

    else:
        print("An error occurred. Try Again.")
    return

def test_findcat(path, name):
    url = URL + path
    req_body = {'name': name}
    resp = requests.post(url, json=req_body)
    if resp.status_code == 200:
        resp = resp.json()  # get a string of the json representation of data
        resp = json.loads(resp)  # convert the JSON representation to a python dictionary for easy indexing
        print(f"Record Found: \n\tID:\t{resp['_id']['$oid']} \n\tNick: \t{resp['name']}\n\tAge: \t{resp['age']}\n\tMajor: \t{resp['major']}")
    elif resp.status_code == 404:
        print(f"Status Code Returned: {resp.status_code} \tA Cat by that nick not in database.")
    else:
        print(f"An error occurred. Try Again. Error code {resp.status_code}")
    return


def test_updatecat(path, find_name, new_name, new_age, new_major):
    url = URL + path
    req_body = {'name': find_name,
                'newName': new_name,
                'age': new_age,
                'major': new_major}
    resp = requests.post(url, json=req_body)
    if resp.status_code == 200:
        print(
            f"Record updated. New Record: \n\tNick: \t{new_name}\n\tAge: \t{new_age}\n\tMajor: \t{new_major}")
        # as written, updatecat only returns a status code. so values are taken from the Proposed changes used in the
        # request
    else:
        print(f"An error occurred. Try Again. Error code {resp.status_code}")
    return


def test_deletecat(path, find_name):
    url = URL + path
    req_body = {'name': find_name}
    resp = requests.post(url, json=req_body)

    ret_msg = json.loads(resp.json())
    print(f"Status Code Returned: {resp.status_code} \t Return Message Body: {ret_msg['Body']}")
    return

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