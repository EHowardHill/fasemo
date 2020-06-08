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

    from_form = False
    aliases = []

    try:
        data = request.get_json()
        usern = data['user']
        passw = data['pass']
        from_form = True
    except:
        try:
            usern = session['user']
            passw = session['pass']
        except:
            usern = ''
            passw = ''

    v = Login.query.filter_by(usern=session['user']).first()
    valid = True if v != None else False

    if valid and from_form:
        session['user'] = usern
        session['pass'] = passw

    refresh_thread()

    return {'connect': True, 'signedin': valid}

@app.route('/post_message', methods=["POST"])
def post_message():

    raw = request.get_json()

    new_message = Messages(
        alias = raw['alias'],
        thread = 1,
        content = raw['message'],
        timestamp = str(datetime.now())
    )

    db.session.add(new_message)
    db.session.commit()

    refresh_thread()

    return {'success':1}

@app.route('/get_aliases', methods=["GET","POST"])
def get_aliases():
    aliases = []
    v = Login.query.filter_by(usern=session['user']).first()
    valid = True if v != None else False

    if valid:
        aliases = []
        values = Alias_Reference.query.filter_by(user=v.id).all()
        for val in values:
            tdict = {}
            x = Alias.query.filter_by(id=val.id).one()
            tdict['name'] = x.name
            tdict['pic_profile'] = x.pic_profile
            tdict['id'] = x.id
            aliases.append(tdict)
        pprint(aliases)

    return {aliases:'Hello?'}

@io.on('refresh')
def refresh_thread():
    mess = Messages.query.limit(100).all()
    mess.reverse()

    output = []
    nn = ''

    for m in mess:
        props = {}
        n = Alias.query.filter_by(id=m.alias).first().name
        if n == nn: props['continue'] = 1
        props['pic'] = Alias.query.filter_by(id=m.alias).first().pic_profile
        props['name'] = n
        props['text'] = m.content
        props['date'] = m.timestamp
        output.append(props)
        nn = n

    io.emit('refresh_thread', json.dumps(output))

if __name__ == "__main__":
    io.run(app)