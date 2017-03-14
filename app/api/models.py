from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate

db = SQLAlchemy()

# Relationships






class Series(db.Model):
    title = db.Column(db.String(250))
    overview = db.Column(db.String(250), nullable=True)
    series_art = (db.String(250), nullable=True)

    def __init__(self, title, overview, series_art):
        self.title = title
        self.overview = overview
        self.series_art = series_art


class SerieSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    title = fields.String(validate=not_blank)
    overview = fields.string()
    # Need to make this field
    #not blank on add
    series_art = fields.String()

    class Meta:
        fields = ('title', 'overview', 'series_art')

class Tags(db.Model):
    tag = db.Column(db.String(250))

class Season(db.model):
    number = db.Column(db.Integer)


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason

if __name__ == "__main__":
    db.create_all()
