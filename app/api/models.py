from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from slugify import slugify

db = SQLAlchemy()

# Relationships

class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tmdb_id = db.Column(db.Integer)
    title = db.Column(db.String(250))
    overview = db.Column(db.String(250), nullable=True)
    series_art = db.Column(db.String(250), nullable=True)
    slug = db.Column(db.String(250))

    def __init__(self, tmdb_id, title, overview, series_art):
        self.tmdb_id = tmdb_id
        self.title = title
        self.overview = overview
        self.series_art = series_art
        self.slug = create_slug(self.title)

    def create_slug(self, title):
        return slugify(title)




class SerieSchema(Schema):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    title = fields.String(validate=not_blank)
    overview = db.Column(db.TEXT())
    # Need to make this field
    #not blank on add
    series_art = fields.String()

    class Meta:
        fields = ('title', 'overview', 'series_art')

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(250))

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    overview = db.Column(db.TEXT())
    art = db.Column(db.String())
    series = db.Column(db.Integer, db.ForeignKey(Series.id))


class Media_File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    path = db.Column(db.String(250))
    slug = db.Column(db.String(250))
    image_path = db.Column(db.String(250))
    overview = db.Column(db.TEXT())
    media_type = db.Column(db.String(250))

    __mapper_args__ = {'polymorphic_on': media_type}

    def __init__(self, title, path, image_path, overview):
        self.title = title
        self.path = path
        self.slug = self.create_slug(title)
        self.image_path = image_path
        self.overview = overview

    def create_slug(self, title):
        return slugify(title)


class Episode(Media_File):
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {'polymorphic_identity': 'Episode'}
    season = db.Column(db.Integer, db.ForeignKey(Season.id))
    episode_number = db.Column(db.Integer)

class Movie(Media_File):
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {'polymorphic_identity': 'Movie'}
    release_date = db.Column(db.Date)
    runtime = db.Column(db.Integer)



def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
