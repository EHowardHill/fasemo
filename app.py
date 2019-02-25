import os, json, mysql
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    print (os.listdir("./"))
    return render_template('index.html')

@app.route('/save_work', methods=['POST'])
def save_work():

    print("Yay! We got here!")

    success = 1
    id = request.form['id']
    content = request.form['content']

    try:
        file = open('./works/' + str(id) + ".htm", 'w+')
        file.write(content)
        file.close()

    except Exception as e:
        print(str(e))
        success = 0

    return json.dumps({'status': success});