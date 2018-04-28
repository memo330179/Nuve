from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response, current_app, send_from_directory
from flask_restful import Api
from app.mod_auth.views import Resource
import flask_restful
from app.mod_auth.views import login_required
from guessit import guessit
from app.api.upload import upload_movie, upload_episode
from app.api.db_functs import add_episode_to_db, add_movie_to_db
from werkzeug.utils import secure_filename
import os
from app.api.models import Series, Season,Episode, Movie, SeriesSchema, SeasonSchema, EpisodeSchema, MovieSchema


media_api = Blueprint('media_api', __name__, static_folder='uploads')
series_schema = SeriesSchema()
season_schema = SeasonSchema()
episode_schema = EpisodeSchema()
movie_schema = MovieSchema()


# we need to upload a file
# this is the simplest way I could do it
@media_api.route("/upload/media", methods=["POST"])
def upload_media():
    print(request.files)
    media_files = request.files

    for i, f in enumerate(request.files):
        media_file = request.files[f]

        # print(media_file)

        filename = secure_filename(media_file.filename)

        guessed_info = guessit(filename)
        if guessed_info['type'] == "movie":
            filepath = upload_movie(media_file)
            add_movie_to_db(filename, guessed_info)
        elif guessed_info['type'] == "episode":
            filepath = upload_episode(media_file, guessed_info)
            add_episode_to_db(filepath, guessed_info)
            
    return "finished"
    
@media_api.route("/stream/<int:media_id>", methods=["GET"])
def stream_file(media_id):
    media = Episode.query.get(media_id)
    print('###############################')
    print(media.media_type)
    print('################################')
    if media.media_type == "Episode":
        return send_from_directory(os.path.join(current_app.root_path, media.path.rsplit('/', 1)[0]), media.path.rsplit('/', 1)[1])
    else:
        return send_from_directory(os.path.join(current_app.root_path, 'uploads/movies'), media.path)


rest_api = Api(media_api)


# Any API class now inheriting the Resource class will need Authentication
class Shows(Resource):

    def get(self):

        results = Series.query.all()
        series = series_schema.dump(results, many=True).data
        return jsonify(series)
        
class Seasons(Resource):
    
    def get(self, series_id):
        
        results = Season.query.filter_by(series=series_id).all()
        seasons = season_schema.dump(results, many=True).data
        return jsonify(seasons)
        
class SeasonObj(Resource):
    def get(self, season_id):
        results = Season.query.get(season_id)
        season = season_schema.dump(results).data
        return jsonify(season)
        
class Episodes(Resource):
    def get(self, season_id):
        results = Episode.query.filter_by(season=season_id)
        print(results[0].title)
        episodes = episode_schema.dump(results, many=True).data
        return jsonify(episodes)
        
class MediaObj(Resource):
    
    def get(self, media_id):
        
        results = Episode.query.get(media_id)
        media = episode_schema.dump(results).data
        return jsonify(media)
        
class Movies(Resource):
    
    def get(self):
        results = Movie.query.with_polymorphic ([Movie]).filter_by(media_type='Movie').all()
        movies = movie_schema.dump(results, many=True).data
        return jsonify(movies)




rest_api.add_resource(Shows, '/shows')
rest_api.add_resource(Seasons, '/seasons/<int:series_id>')
rest_api.add_resource(SeasonObj, '/season/<int:season_id>')
rest_api.add_resource(Episodes, '/episodes/<int:season_id>')
rest_api.add_resource(MediaObj, '/serve/<int:media_id>')
rest_api.add_resource(Movies, '/movies')


