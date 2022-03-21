from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "sanikamal-code1234"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/example_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    course = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, phone, course):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.course = course


@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)


@app.route('/edit/<int:id>')
def edit(id):
    student = Student.query.filter_by(id=id).first()
    if student:
        return render_template('edit.html', student = student)
    return f"Student with id ={id} Doenst exist"

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))
        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.course = request.form['course']
        db.session.commit()
        flash("Student Updated Successfully")
        return redirect(url_for('index'))


@app.route("/live_search", methods=["POST", "GET"])
def live_search():
    if request.method == 'POST':
        word = request.form['query']
        if word == '':
            students = Student.query.all()
        else:
            result = db.session.execute("SELECT * FROM student WHERE first_name LIKE '%%{}%%' OR last_name LIKE '%%{}%%' OR email LIKE '%%{}%%' OR course LIKE '%%{}%%' ORDER BY id DESC".format(word,word,word,word))
    
    return jsonify({'htmlresponse': render_template('response.html', student=result)})


if __name__ == '__main__':
    app.run()
