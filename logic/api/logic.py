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

@app.route('/refresh_thread', methods=["GET","POST"])
def refresh_thread():
    return {
        'message': [
            {'pic':"ac.png",'text':"Now?"},
            {'pic':"ac.png",'text':"How about now?"}
            ]
        }

if __name__ == "__main__":
    app.run()