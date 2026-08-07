import os
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_migrate import Migrate   
from flask_mail import Mail, Message
from threading import Thread

# Create an instance of a Flask application
# It defines the core center for Web requests
# coming from the user's browser
app = Flask(__name__)

# Flask-SQLAlchemy Configuration
app.config['SECRET_KEY'] =  'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = f"Flasky Admin <{os.environ.get('MAIL_USERNAME')}>"
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# It represents the Role model inheriting from db.Model
class Role(db.Model):
     # Overwrite default table name set by Flask-SQLAlchemy
    __tablename__ = 'roles'

    # Table columns 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # On a given instance of Role, this will return an object that 
    # lists all the users that have this role
    users = db.relationship('User', backref='role', lazy='dynamic')

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
    

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# Initialize Bootstrap extension by passing in
# the instance of the app
bootstrap = Bootstrap(app)

# Initialize extension to format dates and times
moment = Moment(app)

# NameForm inherits from FlaskForm
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Allows Flask to inject db, User and Role into the flask shell
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

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
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))

# It handles dynamic routes
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)