from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.secret_key = "sanikamal-code1234"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'example_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('''SELECT * FROM student''')
    students = cur.fetchall()
    return render_template('index.html', students=students)


@app.route("/live_search", methods=["POST", "GET"])
def live_search():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        word = request.form['query']
        if word == '':
            query = "SELECT * from student ORDER BY id"
            cur.execute(query)
            student = cur.fetchall()
        else:
            query = "SELECT * from student WHERE first_name LIKE '%{}%' OR last_name LIKE '%{}%' OR email LIKE '%{}%' OR class LIKE '%{}%' ORDER BY id DESC".format(
                word, word, word, word)
            cur.execute(query)
            student = cur.fetchall()
    return jsonify({'htmlresponse': render_template('response.html', student=student)})


if __name__ == '__main__':
    app.run()
