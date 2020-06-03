from pprint import pprint
from flask import Flask, render_template, request, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy

# Initial DB setup
application = Flask(__name__, template_folder='templates')
application.secret_key = "welcome to the cheese house"          # Arbitrary, can be any string
application.config['SESSION_TYPE'] = 'filesystem'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fasemo.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

# Import SQlAlchemy model classes
from models import Alias, Alias_Reference, Login, Messages, Permissions, Thread

@application.route('/', methods=["GET","POST"])
def start():
    return render_template('landing.htm')

start()