from flask import Flask

# Create an instance of a Flask application
# It defines the core center for Web requests
# coming from the user's browser
app = Flask(__name__)


# The following chunk of code
# is called a route, composed of
# a function view, a handler to be called
# when an event is triggered, in this case a user
# visiting the root of the web application
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'