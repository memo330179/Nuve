# This file brings the various model files into a central place
# this is necessary since I am using the blueprint model to separate model files.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
import app.api.models
import app.mod_auth.models