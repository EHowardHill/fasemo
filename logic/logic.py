from pprint import pprint
from flask import Flask, render_template, request, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime

application = Flask(__name__, template_folder='templates')
application.secret_key = "welcome to the cheese house"          # Arbitrary, can be any string
application.config['SESSION_TYPE'] = 'filesystem'
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://app:Cheesehouse1470!!@localhost/fasemo?charset=utf8'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Login(db.Model):
    __tablename__ = 'login'
    id = Column(Integer, primary_key = True)
    usern = Column(String(45))
    passw = Column(String(45))

def start():
    info = Login.query.filter_by(usern='ethan').first()
    if info.passw == 'Bullwinkle01':
        print('Yay!')
    else:
        print('um, no!')

start()