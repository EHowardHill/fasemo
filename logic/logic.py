from pprint import pprint
from flask import Flask, render_template, request, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

application = Flask(__name__, template_folder='templates')
application.secret_key = "welcome to the cheese house"          # Arbitrary, can be any string
application.config['SESSION_TYPE'] = 'filesystem'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fasemo.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Login(db.Model):
    __tablename__ = 'login'
    usern = Column(String(45), primary_key = True)
    passw = Column(String(45))

def start():
    info = Login.query.filter_by(usern='ethan').first()
    if info.passw == 'Bullwinkle01':
        print('Yay!')
    else:
        print('um, no!')

start()