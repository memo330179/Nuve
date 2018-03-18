from flask import Blueprint, render_template, request, flash, redirect, url_for


frontend = Blueprint('frontend', __name__, template_folder='templates')

@frontend.route("/hello")
def hello():
  return render_template('hello.html')
