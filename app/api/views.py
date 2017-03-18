from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_restful import Resource, Api
import flask_restful
from app.mod_auth.views import login_required

media_api = Blueprint('media_api', __name__)


# we need to upload a file
# this is the simplest way I could do it
@media_api.route("/upload/<media_type>", methods=["POST"])
def upload_media(media_type):
    media_file = request.files['file']
    if media_type = "movie":
        #upload_movie(media_file)
        pass
    else if media_type = "tv":
        #upload_tv(media_file)
        pass



rest_api = Api(media_api)
# Adding the login decorator to the Resource class
class Resource(flask_restful.Resource):
    method_decorators = [login_required]


# Any API class now inheriting the Resource class will need Authentication
class Test(Resource):

    def get(self):

        return jsonify({"test": "test succesful"})




rest_api.add_resource(Test, '/test')
