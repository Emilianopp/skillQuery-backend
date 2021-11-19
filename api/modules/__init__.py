from flask import Flask
from flask.globals import session
import secrets


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex()
    from .role import roles 
    from .location import location
    from .packages import packages
    from .tech import tech
    from .map import map
    from .education import education
    # from .ops  import ops
    app.register_blueprint(roles,url_prefix ='/')
    app.register_blueprint(location,url_prefix = '/')
    app.register_blueprint(tech,url_prefix = '/')
    app.register_blueprint(packages,url_prefix = '/')
    app.register_blueprint(map,url_prefix = '/')
    app.register_blueprint(education,url_prefix = '/')
    # app.register_blueprint(ops,url_prefix = '/')
    return app
