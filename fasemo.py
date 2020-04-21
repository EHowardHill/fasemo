import os, json, mysql.connector as mariadb, pprint, sqlite3, shutil
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():

    for c in cursor:
        entry = c

    return render_template(
        'editor.html',
        book_id = str(entry[1]),
        book_name = str(entry[2]).upper(),
        )