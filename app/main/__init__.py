from flask import Blueprint

# Create a blueprint, passing the module's name (main) 
# and the module's package name (__name__)
main = Blueprint('main', __name__)

# Import views and errors modules
# The dots indicate that the modules are in the same package as __init__.py
from . import views
from . import errors