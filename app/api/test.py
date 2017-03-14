from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, make_response
from flask_restful import Resource, Api
import flask_restful
from app.mod_auth.views import login_required

api = Blueprint('api', __name__)

test_api = Api(api)

# Adding the login decorator to the Resource class
class Resource(flask_restful.Resource):
    method_decorators = [login_required]


# Any API class now inheriting the Resource class will need Authentication
class Test(Resource):

    def get(self):

        return jsonify({"test": "test succesful"})




test_api.add_resource(Test, '/test')
