# Project Installation Instructions

We'll be using Python, I recommend 3.7 or newer. 
To keep the home environment tidy, we'll be using a virtual environment, you can use `conda` or `virtualenv`.
These instructions use `virtualenv` (`venv`).

I am using an IDE (PyCharm) to do a lot of my handling of the virtual environment. 
I recommend this only because it is one less thing to worry about. 

## Step 1: Setting Up Virtual Environment
In this step, we'll initialize our virtual environment and install required packages.
I chose to use an IDE for this because setting up and activating the virtual environment is done automatically. 
This can ensure that our packages are localized and we won't run into any dependency issues.
### Initializing Virtual Environment
This can be done one of two ways: 1) Manually using `virtualenv` (or `conda`) or, 2) Automatically when creating a project
in your favorite IDE.

For manual set up, please refer to: https://towardsdatascience.com/virtual-environments-104c62d48c54.
This article gets into both the "how to use" and the "why we use" virtual environments with Python.
If you run into a paywall, please visit https://12ft.io/ to remove it.

As for the automatic setup, this will vary slightly depending on IDE used: 
- In your IDE, select "New Project" or "New Folder" or similar wording
- Usually in this screen or the next, when you select your language, 
you will be given an option to create a virtual environment
  - For PyCharm, it is directly under Location choice.

## Step 2: Cloning the Repo
You can clone the repo using HTTPS using:

```git clone https://github.com/arusk2/cat_api_practice.git```

Alternatively, you can set up SSH keys in your Github account and clone using SSH. I prefer this method 
but takes set up that isn't covered here. You can clone via SSH using:

```git clone git@github.com:arusk2/cat_api_practice.git```

Our repo structure has three important files:
- **api_final.py**: a final version of the API practice code, all filled in. I'm choosing to include this as a reference.
- **api.py**: a skeleton from the api_final.py that is needs code added. I've tried to include notes and prompts where code
  is needed. Some specifics, like the way we reference our database, have been filled in so that we're focusing on the broad
  strokes of the API building process and not the library-specific implementations.
- **requirements.txt**: This we will be using to install dependencies
## Step 3: Making a New Branch
If you want to use git to track your changes, it will be best to do so on your own branch. In order to do this, 
navigate to the project directory using 
``` cd cat_api_test``` (if you haven't already). Then, use the following command:

```git checkout -b YourNick```

`checkout` is the command that will switch a tracked branch in Git and the `-b` flag will create a new branch with the name that follows it. The name should be all one word. 
Just switch our "YourNick" with, well, your cat nick (This can also be whatever unique name you want your branch 
to be named, just know I will be able to see it).
## Step 4: Installing Dependencies
Now that we have our virtual environment created, our IDE has automatically activated it. You can double check this by
opening a terminal in your IDE and verify that you have something like:
```(your environment name) shell_name_here $ ```. This will vary slightly based on terminal language but the important 
thing to see if the name of your virtual environment in parentheses before everything. This shows that its been activated.

Now, we will be using `pip` to install our dependencies from the repo. `pip` is the default package manager for Python.
You can install dependencies using:

```pip install -r requirements.txt```

I have included in our repo a list of dependencies needed for the project, this will install all of them automatically 
to your virtual environment. This is a fresh environment, so we _shouldn't_ run into any issues.

## Step 5: Testing Dependencies
We're going to be working on `api.py`, it is a skeleton of the code and won't run successfully until we add code to it.
There is a finalized version called `api_final.py` that has all the filled in code.
This can be used for reference and is very useful for testing to make sure our requirements are successfully installed.

To test that we have successfully installed all requirements, run the command:

```flask --app api_final.py --debug run```

This will create a Flask webserver using the `api_final.py` code. We can then run
```python test.py``` to start a training script that we can manually test the API. If you are getting status codes of 200 as returns, you
should be good to go!

To run the `api.py` file, you can use the python script `flask_start.py` by using the command:

```python flask_start.py ```

**NOTE: This will not work until we add code to it. You will get 404 errors.**

## Windows tips

start the server in powershell with the password env var:

```powershell
$Env:DB_PASS = '' # put your password here, not in the source code. Sure it ends up in your terminal history, but that's a less public place.
flask --app api.py --debug run
```

JSON requires the outer double quotes, and powershell eats them. To curl from powershell:
curl.exe --data-binary '"{ \"first\": 2, \"second\": 2 }"' -v -H "Content-Type: application/json" localhost:5000/add
curl.exe --data-binary '"{ \"name\": \"a\", \"age\": 1, \"major\": \"a\" }"' -v -H "Content-Type: application/json" localhost:5000/newcat

## Linux tips

start the server in bash with the password env var:

```sh
DB_PASS='' # put your password here, not in the source code. Sure it ends up in your terminal history, but that's a less public place
flask --app api.py --debug run
```
