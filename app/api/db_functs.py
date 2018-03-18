import tmdb_funcs
import os
from models import *
from slugify import slugify
from sqlalchemy import and_
from tmdb_functs import *

def add_episode_to_db(filepath, guessed_info):
   # search for tv show
   tmdb_info = search_show(guessed_info.title)[0]
   # check if exists
   if not series_exists(tmdb_info['id']):
      series = Series(tmdb_info['id'], tmdb_info['title'],
                      tmdb_info['overview'], tmdb_info['series_art'])
   # add to db~                              |                                                                                                                                      
   if not season_exists(tmdb_info['id'], guessed_info['season']):
      tmdb_season = get_season_info(tmdb_info['id'], guessed_info['season'])[0]
      season = Season(tmdb_season['season_number'], tmdb_season['overview'], tmdb_season['poster_path'], tmdb_info['id']) 
   # check if exists
   # search for season
   # add to db

   # search for episode
   if not episode_exists(tmdb_info['id'], guessed_info['season'], guessed_info['episode']):
     tmdb_season = get_episode_info(tmdb_info['id'], guessed_info['season'], guessed_info['episode'])[0]
     episode = Episode(tmdb_info['id'])
   
   # add to db 


   pass 

def series_exists(series_id):
    series = Series.query.filter_by(id == series_id).scalar()
    return series is not None

def season_exists(series_id, number):
    season_exists = (Season
                     .query
                     .filter_by(and_
                                (series == series_id
                                 ,numer==number))
                     .scalar())
    return season_exists is not None
    
def episode_exists(series_id, season, episode_number):
  season_exists = (Episode
                     .query
                     .filter_by(and_
                                (series == series_id
                                 ,season==season, episode_number=episode_number))
                     .scalar())
  return season_exists is not None