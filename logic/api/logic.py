from json import loads
from datetime import datetime
from pprint import pprint
from flask import Flask, render_template, request, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy

# Initial DB setup
app = Flask(__name__, template_folder='templates')
app.secret_key = "welcome to the cheese house"          # Arbitrary, can be any string
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fasemo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import SQlAlchemy model classes
from models import Alias, Alias_Reference, Login, Messages, Permissions, Thread

@app.route('/refresh_thread', methods=["POST"])
def refresh_thread():

    mess = Messages.query.limit(100).all()

    output = [
        {
            'pic': Alias.query.filter_by(id=m.alias).first().pic_profile,
            'text': m.content
        } for m in mess if m != None
    ]

    return {'message':output}

@app.route('/post_message', methods=["POST"])
def post_message():

    raw = request.get_json()

    new_message = Messages(
        alias = 1,
        thread = 1,
        content = raw['message'],
        timestamp = str(datetime.now())
    )

    db.session.add(new_message)
    db.session.commit()

    return {'success':1}

if __name__ == "__main__":
    app.run()