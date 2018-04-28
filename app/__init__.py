# Defines the app creator to use with blueprint

from flask import Flask
from flask_cors import CORS


# http://flask.pocoo.org/docs/0.10/patterns/appfactories/
def create_app(config_filename):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/media_api/*": {"origins": "*"},r"/api/*": {"origins": "*"},r"/upload/*": {"origins": "*"}},)
    app.config.from_object(config_filename)

    # Init SQLAlchemy
    from app.db_base import db
    db.init_app(app)

    # Blueprints

    from app.mod_auth.views import mod_auth
    app.register_blueprint(mod_auth, url_prefix='/api')
    from app.api.views import media_api
    app.register_blueprint(media_api, url_prefix='/media_api')

    return app
