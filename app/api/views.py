from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_restful import Resource, Api
import flask_restful
from app.mod_auth.views import login_required
from guessit import guessit

media_api = Blueprint('media_api', __name__)


# we need to upload a file
# this is the simplest way I could do it
@media_api.route("/upload/media", methods=["POST"])
def upload_media(media_type):
    media_files = request.files['file[]']

    for media_file in media_files:

        filename = secure_filename(media_file.filename)

        guessed_info = guessit(filename)

        if guessed_info.type == "Movie":
            upload_movie(media_file)
        elif guessed_info.type == "Episode":
            upload_tv(media_file, guessed_info)


rest_api = Api(media_api)
# Adding the login decorator to the Resource class
class Resource(flask_restful.Resource):
    method_decorators = [login_required]


# Any API class now inheriting the Resource class will need Authentication
class Test(Resource):

    def get(self):

        return jsonify({"test": "test succesful"})




rest_api.add_resource(Test, '/test')
