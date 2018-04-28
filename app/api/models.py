from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, validate
from slugify import slugify
from app.db_base import db

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
        self.slug = self.create_slug(self.title)

    def create_slug(self, title):
        return slugify(title)




class SeriesSchema(Schema):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    title = fields.String(validate=not_blank)
    overview = db.Column(db.TEXT())
    # Need to make this field
    #not blank on add
    series_art = fields.String()

    class Meta:
        fields = ('id', 'title', 'overview', 'series_art')

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(250))

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    overview = db.Column(db.TEXT())
    art = db.Column(db.String())
    series = db.Column(db.Integer, db.ForeignKey(Series.id))
    
    def __init__(self, number, overview, art, series):
        self.number = number 
        self.overview = overview
        self.art = art
        self.series = series
        
class SeasonSchema(Schema):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    number = fields.Integer(validate=not_blank)
    overview = db.Column(db.TEXT())
    # Need to make this field
    #not blank on add
    art = fields.String()

    class Meta:
        fields = ('id', 'number', 'overview', 'art')
        


class Media_File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250))
    slug = db.Column(db.String(250))
    path = db.Column(db.String(250))
    image_path = db.Column(db.String(250))
    overview = db.Column(db.TEXT())
    media_type = db.Column(db.String(250))

    __mapper_args__ = {'polymorphic_on': media_type}



class Episode(Media_File):
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {'polymorphic_identity': 'Episode'}
    season = db.Column(db.Integer, db.ForeignKey(Season.id))
    episode_number = db.Column(db.Integer)
    
    def __init__(self, title, path, image_path, overview, season, episode_number, tmdb_id):
        self.title = title
        self.slug = self.create_slug(title)
        self.path = path
        self.image_path = image_path
        self.overview = overview
        self.season = season
        self.episode_number = episode_number
        self.tmdb_id = tmdb_id

    def create_slug(self, title):
        return slugify(title)
        
class EpisodeSchema(Schema):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    title = fields.String(validate=not_blank)
    path = fields.String(validate=not_blank)
    overview = fields.String()
    episode_number = fields.Integer()
    # Need to make this field
    #not blank on add
    image_path = fields.String()

    class Meta:
        fields = ('id', 'title','path', 'overview', 'episode_number', 'image_path')

class Movie(Media_File):
    __table_args__ = {'extend_existing': True}
    __mapper_args__ = {'polymorphic_identity': 'Movie'}
    release_date = db.Column(db.Date)
    runtime = db.Column(db.Integer)
    
    def __init__(self, title, path, image_path, overview, release_date, runtime, tmdb_id):
        self.title = title
        self.path = path
        self.slug = self.create_slug(title)
        self.image_path = image_path
        self.overview = overview
        self.release_date = release_date
        self.runtime = runtime
        self.tmdb_id = tmdb_id

    def create_slug(self, title):
        return slugify(title)
        
class MovieSchema(Schema):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    title = fields.String(validate=not_blank)
    path = fields.String(validate=not_blank)
    overview = db.Column(db.TEXT())
    episode_number = fields.Integer()
    # Need to make this field
    #not blank on add
    image_path = fields.String()

    class Meta:
        fields = ('id', 'title','path', 'overview', 'episode_number', 'image_path')

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
