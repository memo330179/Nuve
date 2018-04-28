from .tmdb_funcs import * 
import os
from .models import *
from slugify import slugify
from sqlalchemy import and_
from datetime import datetime


def add_episode_to_db(filepath, guessed_info):
   """ Adds the episode information to the database along with show and season information"""
   tmdb_info = search_show(guessed_info['title'])['results'][0]
   
   # Insert series information 
   if not series_exists(tmdb_info['id']):
      series = Series(tmdb_info['id'], tmdb_info['name'],
                      tmdb_info['overview'], tmdb_info['poster_path'])
   else:
       series = Series.query.filter_by(tmdb_id=tmdb_info['id']).first()
                              |
   db.session.add(series)
   
   # add season information
   if not season_exists(series.id, guessed_info['season']):
      tmdb_season = get_season_info(tmdb_info['id'], guessed_info['season'])
      season = Season(tmdb_season['season_number'], tmdb_season['overview'], tmdb_season['poster_path'], series.id) 
      db.session.add(season)
   else:
      season = Season.query.filter(and_(Season.series == series.id, number == number))

   # Add episode information
   if not episode_exists(season.id, guessed_info['episode']):
     tmdb_episode = get_episode_info(tmdb_info['id'], guessed_info['season'], guessed_info['episode'])
     episode = Episode(tmdb_episode['name'], filepath, tmdb_episode['still_path'], tmdb_episode['overview'], season.id,tmdb_episode['episode_number'], tmdb_episode['id'])
     db.session.add(episode)
     
   session_commit()
   
def add_movie_to_db(filepath, guessed_info):
    """Adds the movie to the database """
  
    if not movie_exists(filepath):
        tmdb_movie = get_movie_info(search_movie(guessed_info['title'])['results'][0]['id'])
        movie = Movie(tmdb_movie['title'], filepath, tmdb_movie['poster_path'], tmdb_movie['overview'], datetime.strptime(tmdb_movie['release_date'],"%Y-%m-%d"),tmdb_movie['runtime'], tmdb_movie['id'])
        db.session.add(movie)
        session_commit()
        

def series_exists(series_id):
    """Returns True if the series is already in the database to avoid duplicates"""
    series = Series.query.filter_by(id=series_id).scalar()
    return series is not None

def season_exists(series_id, number):
    """ Returns True of the season is already in the database to avoid duplicates"""
    season_exists = (Season
                     .query
                     .filter(and_
                                (Season.series == series_id
                                 , number ==number))
                     .scalar())
    return season_exists is not None
    
def episode_exists(season_id, episode_number):
    """ Returns True of the episode is already in the database to avoid duplicates"""
  season_exists = (Episode
                     .query
                     .filter(and_
                                (Episode.season==season_id, Episode.episode_number==episode_number))
                     .scalar())
  return season_exists is not None
  
def movie_exists(filepath):
    """ Returns True of the movie is already in the database to avoid duplicates"""
  exists = (Movie
                     .query
                     .filter(Movie.path == filepath)
                     .scalar())
  return exists is not None