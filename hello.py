from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create an instance of a Flask application
# It defines the core center for Web requests
# coming from the user's browser
app = Flask(__name__)
# WTF mechanism for security reasons
app.config['SECRET_KEY'] =  'hard to guess string'

# Initialize Bootstrap extension by passing in
# the instance of the app
bootstrap = Bootstrap(app)

# Initialize extension to format dates and times
moment = Moment(app)

# NameForm inherits from FlaskForm
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

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
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.now(timezone.utc), form=form, name=session.get('name'))

# It handles dynamic routes
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)