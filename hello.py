import os
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, session, redirect, url_for, flash
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

# Flask-SQLAlchemy Configuration
app.config['SECRET_KEY'] =  'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# It represents the Role model inheriting from db.Model
class Role(db.Model):
     # Overwrite default table name set by Flask-SQLAlchemy
    __tablename__ = 'roles'

    # Table columns 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # On a given instance of Role, this will return an object that 
    # lists all the users that have this role
    users = db.relationship('User', backref='role')

    # Used for debugging and testing purposes 
    def __repr__(self):
        return '<Role %r>' % self.name

# It represents the User model inheriting from db.Model
class User(db.Model):
    # Overwrite default table name set by Flask-SQLAlchemy
    __tablename__ = 'users'

    # Table columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    # Foreign key column, established relationship between 
    # User and Role models
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # Used for debugging and testing purposes
    def __repr__(self):
        return '<User %r>' % self.username
    


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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('You have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.now(timezone.utc), form=form, name=session.get('name'))

# It handles dynamic routes
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)