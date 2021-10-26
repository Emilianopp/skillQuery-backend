from flask import Flask 


def create_app():
    app = Flask(__name__)
    from .dropdown import roles 
    from .location import location
    app.register_blueprint(roles,url_prefix ='/')
    app.register_blueprint(location,url_prefix = '/')
    return app
