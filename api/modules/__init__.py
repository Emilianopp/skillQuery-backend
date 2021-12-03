from flask import Flask

import secrets
from flask import Flask, session
from flask_session import Session
from  flask_cors import CORS, cross_origin
from datetime import timedelta
import os 

def create_app():
    app = Flask(__name__)
    sess = Session(app)
    app.config.from_object(__name__)
    # app.config['SESSION_COOKIE_PATH'] = '/'
    app.config['SESSION_REFRESH_EACH_REQUEST'] = False
    app.config['SESSION_COOKIE_NAME'] = "my_session"
    app.config['SESSION_COOKIE_DOMAIN'] = "skillquery.herokuapp.com"
    app.secret_key = 'test'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
    sess.init_app(app)
    CORS(app)
    from .role import roles 
    from .location import location
    from .packages import packages
    from .tech import tech
    from .map import map
    from .education import education
    from .ops  import ops

    app.register_blueprint(roles,url_prefix ='/')
    app.register_blueprint(location,url_prefix = '/')
    app.register_blueprint(tech,url_prefix = '/')
    app.register_blueprint(packages,url_prefix = '/')
    app.register_blueprint(map,url_prefix = '/')
    app.register_blueprint(education,url_prefix = '/')
    app.register_blueprint(ops,url_prefix = '/')
    return app
