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
movie_schame = MovieSchema()


# we need to upload a file
# this is the simplest way I could do it
@media_api.route("/upload/media", methods=["POST"])
def upload_media():
    media_files = request.files.getlist('file[]')
    print(media_files)

    for media_file in media_files:
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
    
@media_api.route("/stream/<path:video_path>", methods=["GET"])
def get_file(video_path):
    return send_from_directory(os.path.join(current_app.root_path, 'uploads/shows/futurama/1/'), 'futurama.s1e1.mp4')


rest_api = Api(media_api)


# Any API class now inheriting the Resource class will need Authentication
class Shows(Resource):

    def get(self):

        results = Series.query.all()
        series = series_schema.dump(results, many=True).data
        return jsonify({"series": series})
        
class Seasons(Resource):
    
    def get(self, series_id):
        
        results = Season.query.filter_by(series=series_id).all()
        seasons = season_schema.dump(results, many=True).data
        return jsonify({"seasons": seasons})
        
class SeasonObj(Resource):
    def get(self, season_id):
        results = Season.query.get(season_id)
        season = season_schema.dump(results).data
        return jsonify({'season':season})
        
class Episodes(Resource):
    def get(self, season_id):
        results = Episode.query.filter_by(season=season_id)
        print(results[0].title)
        episodes = episode_schema.dump(results, many=True).data
        return jsonify({'episodes': episodes})
        
class EpisodeObj(Resource):
    
    def get(self, episode_id):
        
        results = Episode.query.get(episode_id)
        episode = episode_schema.dump(results).data
        return jsonify({"episode": episode})




rest_api.add_resource(Shows, '/shows')
rest_api.add_resource(Seasons, '/seasons/<int:series_id>')
rest_api.add_resource(SeasonObj, '/season/<int:season_id>')
rest_api.add_resource(Episodes, '/episodes/<int:season_id>')
rest_api.add_resource(EpisodeObj, '/episode/<int:episode_id>')


