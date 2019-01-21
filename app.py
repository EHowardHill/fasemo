import pprint, json
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    content = ""

    try:
        content = request.form['content']

    except Exception as e:
        print(str(e))

    pprint.pprint(content)
    return render_template('index.html')