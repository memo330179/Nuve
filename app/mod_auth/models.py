# This handles the definition for the models used in authentication. Just the user models.

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from app.db_base import db
from werkzeug.security import generate_password_hash

# Relationships


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_enabled = db.Column(db.Boolean(), nullable=False,
                           server_default='False')

    def __init__(self, email, name, password, is_enabled=False):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
        self.is_enabled = is_enabled

    def add(self, user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, user):
        db.session.delete(user)
        return session_commit()

    def is_active(self):
        return self.is_enabled


class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    name = fields.String(validate=not_blank)
    email = fields.Email()
    # Need to make this field
    #not blank on add
    password = fields.String()
    is_active = fields.Boolean(validate=not_blank)
    role = fields.String()

    class Meta:
        fields = ('id', 'email', 'name', 'is_enabled')


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason

if __name__ == "__main__":
    db.create_all()
