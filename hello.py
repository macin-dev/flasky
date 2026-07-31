from flask import Flask, render_template
from flask_bootstrap import Bootstrap

# Create an instance of a Flask application
# It defines the core center for Web requests
# coming from the user's browser
app = Flask(__name__)

# Initialize Bootstrap extension by passing in
# the instance of the app
bootstrap = Bootstrap(app)

# The following chunk of code
# is called a route, composed of
# a function view, a handler to be called
# when an event is triggered, in this case a user
# visiting the root of the web application
@app.route('/')
def index():
    return render_template('index.html')

# It handles dynamic routes
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)