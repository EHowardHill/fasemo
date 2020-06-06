import logging, json
from json import loads
from time import sleep
from datetime import datetime
from pprint import pprint
from flask import Flask, render_template, request, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, emit, send

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

print("Ahoy!")
clients = []

# Initial DB setup
app = Flask(__name__, template_folder='templates')
app.secret_key = "welcome to the cheese house"          # Arbitrary, can be any string
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fasemo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
io = SocketIO(app, cors_allowed_origins='*')

# Import SQlAlchemy model classes
from models import Alias, Alias_Reference, Login, Messages, Permissions, Thread

ROOMS = {}

@app.route('/connect', methods=["GET", "POST"])
def connected():
    return {'connect': True, 'signedin': False}

@io.on('refresh')
def refresh_thread():

    mess = Messages.query.limit(100).all()

    output = [
        {
            'pic': Alias.query.filter_by(id=m.alias).first().pic_profile,
            'text': m.content
        } for m in mess if m != None
    ]

    io.emit('thread', json.dumps(output), session['room'])

@app.route('/post_message', methods=["POST"])
def post_message():

    raw = request.get_json()

    new_message = Messages(
        alias = session['alias'],
        thread = 1,
        content = raw['message'],
        timestamp = str(datetime.now())
    )

    db.session.add(new_message)
    db.session.commit()

    send_messages()
    refresh_thread()

    return {'success':1}

def send_messages():
    mess = Messages.query.limit(100).all()
    mess.reverse()

    output = [
        {
            'pic': Alias.query.filter_by(id=m.alias).first().pic_profile,
            'text': m.content
        } for m in mess if m != None
    ]

    io.emit('refresh_thread', json.dumps(output))

if __name__ == "__main__":
    io.run(app)