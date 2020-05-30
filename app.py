import os
from flask import Flask

def create_app():
    # create and configure the app
    app = Flask(__name__)

    # use Blueprint separate file (views.py)
    with app.app_context():
        from apps.routing.views import blah_bp
        app.register_blueprint(blah_bp)

    return app

