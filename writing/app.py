import os, json, mysql.connector as mariadb, pprint, sqlite3, shutil
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    
    works = mariadb.connect(
        user='root',
        password='Shebang01#!',
        database='works')
    cursor = works.cursor()
    resp = cursor.execute("select * from books")
    
    # 0 - Author
    # 1 - ID
    # 2 - Name
    # 3 - Description

    for c in cursor:
        entry = c

    return render_template(
        'editor.html',
        book_id = str(entry[1]),
        book_name = str(entry[2]).upper(),
        )

@app.route('/save_work', methods=['POST'])
def save_work():

    success = 1
    id = request.form['id']
    content = request.form['content']

    print("I'm here!")

    #try:
    if True:
        path = './works/' + str(id)

        if not os.path.exists(path):
            os.mkdir(path)
            shutil.copyfile('./templates/chapters.db', path + '/chapters.db')

        conn = sqlite3.connect(path + '/chapters.db')


        conn_l = conn.cursor()
        conn_l.execute('select * from list')
        count = len(conn_l.fetchall())

        # If there are no chapters
        if count == 0:
            conn_l.execute("INSERT INTO list VALUES (?,?,?,?)",
                           (count + 1, 0, 'untitled', datetime.now()))
            conn.commit()

        file = open('./works/' + str(id) + "/01.htm", 'w+')
        file.write(content)
        file.close()
        print("Written!")

    #except Exception as e:
    #    print(str(e))
    #    success = 0

    print("Done!")

    return json.dumps({'status': success});