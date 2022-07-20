# importing flask
from flask import Flask

# create a new flask instance
app = Flask(__name__)

# create flask routes
@app.route('/')
def hello_world():
    return 'Hello world'


