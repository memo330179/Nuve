from flask import Flask


# http://flask.pocoo.org/docs/0.10/patterns/appfactories/
def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    # Init SQLAlchemy
    from app.mod_auth.models import db
    db.init_app(app)

    # Blueprints

    from app.mod_auth.views import mod_auth
    app.register_blueprint(mod_auth, url_prefix='/api')
    from app.api.test import api
    app.register_blueprint(api, url_prefix='/test')

    return app
