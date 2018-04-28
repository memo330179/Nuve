import guessit
import tmdbsimple as tmdb
from urllib.error import HTTPError

try:
    from app import secrets
except ImportError:
    print("The secret file does not exist")


# import and test the movie database 
try:
    tmdb.API_KEY = secrets.TMDB_API_KEY
    print(("using API KEY", tmdb.API_KEY))
    movie = tmdb.Movies(603) #the matrix
    movie.info()
except HTTPError:
    try:
        tmdb.API_KEY = settings.TMDB_API_KEY
        movie = tmdb.Movies(603) #the matrix
        movie.info()
    except HTTPError:
        raise NoAPIKeyFound('No API key was found in setting on in the secret file')


def guess_name(filename):
    movie_info = guessit(filename)
    return movie_info

def search_movie(movie_name):
    search = tmdb.Search()
    return search.movie(query=movie_name)

def get_movie_info(movie_id):
    movie = tmdb.Movies(movie_id)
    response = movie.info()
    return response

def search_show(show_title):
    search = tmdb.Search()
    return search.tv(query=show_title)

def get_show_details(show_id):
    show = tmdb.TV(show_id)
    response = show.info()
    return response

def get_season_info(show_id, season_number):
    season = tmdb.TV_Seasons(show_id, season_number)
    response = season.info()
    return response

def get_episode_info(show_id, season_number, episode_number):
    episode = tmdb.TV_Episodes(show_id, season_number, episode_number)
    response = episode.info()
    return response
