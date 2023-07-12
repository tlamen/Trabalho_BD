import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        # user=os.environ['DB_USERNAME'],
        # password=os.environ['DB_PASSWORD'])
        user= "bernardo",
        password= "Senha123")
    return conn


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/departments')
def departments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM departments;')
    departments = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('departments.html', departments=departments)

@app.route('/professors')
def professors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM professors;')
    professors = cur.fetchall()
    cur.close()
    cur = conn.cursor()
    cur.execute('SELECT * FROM departments;')
    departments = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('professors.html', professors=professors, departments=departments)

@app.route('/disciplines/<int:DEPARTMENT_ID>')
def disciplines(DEPARTMENT_ID):
    conn = get_db_connection()

    cur = conn.cursor()
    sql = "SELECT * FROM disciplines WHERE department_id = " + str(DEPARTMENT_ID) + ";"
    cur.execute(sql)
    disciplines = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    sql = "SELECT * FROM departments WHERE department_id = " + str(DEPARTMENT_ID) + ";"
    cur.execute(sql)
    departments = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute('SELECT * FROM classes;')
    classes = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute('SELECT * FROM professors;')
    professors = cur.fetchall()
    cur.close()

    conn.close()
    return render_template('disciplines.html', disciplines=disciplines, departments=departments, classes=classes, professors=professors)

@app.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        curso = request.form['curso']
        email = request.form['email']
        senha = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO students (student_name, curso, email, password)'
                    'VALUES (%s, %s, %s, %s)',
                    (nome, curso, email, senha))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('register.html')
    
@app.route('/review/<int:CLASS_ID>', methods=('GET', 'POST'))
def review(CLASS_ID):
    if request.method == 'POST':
        grade = int(request.form['grade'])
        message = request.form['message']
        email = request.form['email']
        senha = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        sql = "SELECT student_id, password FROM students WHERE email = '" + email + "';"
        cur.execute(sql)
        resgatada = cur.fetchone()
        print(resgatada)
        if senha == resgatada[1]:
            cur.execute('INSERT INTO reviews (grade, message, student_id, class_id)'
                        'VALUES (%s, %s, %s, %s)',
                        (grade, message, resgatada[0], CLASS_ID))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('review', CLASS_ID=CLASS_ID))

    conn = get_db_connection()

    cur = conn.cursor()
    sql = "SELECT * FROM CLASS_VIEW WHERE class_id = " + str(CLASS_ID) + ";"
    cur.execute(sql)
    classe = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    cur.execute('SELECT * FROM students;')
    students = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    sql = "SELECT * FROM REVIEW_VIEW WHERE class_id = " + str(CLASS_ID) + ";"
    cur.execute(sql)
    reviews = cur.fetchall()
    cur.close()

    cur = conn.cursor()
    sql = "SELECT ROUND(AVG(grade), 2), COUNT(*) FROM REVIEW_VIEW WHERE class_id = " + str(CLASS_ID) + ";"
    cur.execute(sql)
    media = cur.fetchall()
    cur.close()

    conn.close()
    return render_template('reviews.html', classe=classe, students=students, reviews=reviews, media=media)