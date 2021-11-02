from flask import Flask
from flask.globals import session
from .Analysis_Processing.Analysis_Processing import *
import secrets


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex()
    from .role import roles 
    from .location import location
    app.register_blueprint(roles,url_prefix ='/')
    app.register_blueprint(location,url_prefix = '/')
    return app
