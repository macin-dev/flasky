from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone

# Create an instance of a Flask application
# It defines the core center for Web requests
# coming from the user's browser
app = Flask(__name__)

# Initialize Bootstrap extension by passing in
# the instance of the app
bootstrap = Bootstrap(app)

# Initialize extension to format dates and times
moment = Moment(app)

# Error handling, it returns a tuple with the
# status code for the response to the client
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# The following chunk of code
# is called a route, composed of
# a function view, a handler to be called
# when an event is triggered, in this case a user
# visiting the root of the web application
@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.now(timezone.utc))

# It handles dynamic routes
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)