import os
import psycopg2
import csv

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        # user=os.environ['DB_USERNAME'],
        # password=os.environ['DB_PASSWORD'])
        user= "bernardo",
        password= "Senha123")


# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS students;')
cur.execute('CREATE TABLE students (student_id serial PRIMARY KEY,'
                                 'student_name varchar (50) NOT NULL,'
                                 'curso varchar (100) NOT NULL,'
                                 "is_admin bit DEFAULT '0',"
                                 'email varchar(150) NOT NULL UNIQUE,'
                                 'password varchar(30) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS departments;')
cur.execute('CREATE TABLE departments (department_id serial PRIMARY KEY,'
                                 'codigo INT NOT NULL UNIQUE,'
                                 'department_name varchar (150) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

with open('./ofertas_sigaa/data/2023.1/departamentos_2023-1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            sql = "INSERT INTO departments (codigo, department_name) VALUES (" + row[0] + " , '" + row[1] + "');"
            cur.execute(sql)

cur.execute('DROP TABLE IF EXISTS disciplines;')
cur.execute('CREATE TABLE disciplines (discipline_id serial PRIMARY KEY,'
                                 'discipline_name varchar (150) NOT NULL,'
                                 'codigo varchar(50) NOT NULL,'
                                 'department_id INT NOT NULL,'
                                 'CONSTRAINT fk_department '
                                    'FOREIGN KEY(department_id)' 
                                    'REFERENCES departments(department_id), '
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

with open('./ofertas_sigaa/data/2023.1/disciplinas_2023-1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            sql = "INSERT INTO disciplines (codigo, discipline_name, department_id) VALUES ('"+ row[0] + "' , '" + row[1] + "', (SELECT department_id FROM departments WHERE codigo = " + row[2] + "));"
            cur.execute(sql)

cur.execute('DROP TABLE IF EXISTS professors;')
cur.execute('CREATE TABLE professors (professor_id serial PRIMARY KEY,'
                                 'professor_name varchar (150) NOT NULL,'
                                 'department_id INT NOT NULL,'
                                 'CONSTRAINT fk_department '
                                    'FOREIGN KEY(department_id)' 
                                    'REFERENCES departments(department_id), '
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS classes;')
cur.execute('CREATE TABLE classes (class_id serial PRIMARY KEY,'
                                 'number varchar (10) NOT NULL,'
                                 'discipline_id INT NOT NULL,'
                                 'professor_id INT NOT NULL,'
                                 'CONSTRAINT fk_discipline '
                                    'FOREIGN KEY(discipline_id) ' 
                                    'REFERENCES disciplines(discipline_id), '
                                 'CONSTRAINT fk_professor '
                                    'FOREIGN KEY(professor_id) ' 
                                    'REFERENCES professors(professor_id), '
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

professores_adicionados = []
with open('./ofertas_sigaa/data/2023.1/turmas_2023-1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            if row[2] not in professores_adicionados:
                sql = "INSERT INTO professors (professor_name, department_id) VALUES ('"+ row[2] + "' , (SELECT department_id FROM departments WHERE codigo = " + row[8] + "))"
                cur.execute(sql)
                professores_adicionados.append(row[2])
            sql = "INSERT INTO classes (number, discipline_id, professor_id) VALUES ('"+ row[0] + "' , (SELECT discipline_id FROM disciplines WHERE codigo = '" + row[7] + "' LIMIT 1), (SELECT professor_id FROM professors WHERE professor_name = '" + row[2] + "' LIMIT 1));"
            cur.execute(sql)
            line_count += 1

cur.execute('DROP TABLE IF EXISTS reviews;')
cur.execute('CREATE TABLE reviews (review_id serial PRIMARY KEY,'
                                 'message text NOT NULL,'
                                 'grade int NOT NULL,'
                                 'student_id INT NOT NULL,'
                                 'class_id INT NOT NULL,'
                                 'CONSTRAINT fk_student '
                                    'FOREIGN KEY(student_id)' 
                                    'REFERENCES students(student_id),'
                                 'CONSTRAINT fk_class '
                                    'FOREIGN KEY(class_id)' 
                                    'REFERENCES classes(class_id),'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS reports;')
cur.execute('CREATE TABLE reports (report_id serial PRIMARY KEY,'
                                 'message text NOT NULL,'
                                 'student_id INT NOT NULL,'
                                 'review_id INT NOT NULL,'
                                 'CONSTRAINT fk_students '
                                    'FOREIGN KEY(student_id)' 
                                    'REFERENCES students(student_id),'
                                 'CONSTRAINT fk_review '
                                    'FOREIGN KEY(review_id)' 
                                    'REFERENCES reviews(review_id),'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into tables

# Users

cur.execute('INSERT INTO students (student_name, curso, is_admin, email, password)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Pessoa administradora',
             'Administração',
             '1',
             'admin@unb.com.br',
             'Admin123')
            )

cur.execute('INSERT INTO students (student_name, curso, is_admin, email, password)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Pessoa administradora 2',
             'Administração',
             '1',
             'admin2@unb.com.br',
             'Admin321')
            )

cur.execute('INSERT INTO students (student_name, curso, is_admin, email, password)'
            'VALUES (%s, %s, %s, %s, %s)',
            ('Pessoa estudante',
             'Pedagogia',
             '0',
             'notadmin@unb.com.br',
             'Senha123')
            )

# Reviews

cur.execute('INSERT INTO reviews (message, grade, student_id, class_id) '
            'VALUES (%s, %s, %s, %s)',
            ('Muito boa!!',
             5,
             1,
             1)
            )

cur.execute('INSERT INTO reviews (message, grade, student_id, class_id)'
            'VALUES (%s, %s, %s, %s)',
            ('Mais ou menos.',
             3,
             2,
             1)
            )

cur.execute('INSERT INTO reviews (message, grade, student_id, class_id)'
            'VALUES (%s, %s, %s, %s)',
            ('Mais pra menos do que pra mais.',
             2,
             3,
             1)
            )

# Reports

cur.execute('INSERT INTO reports (message, student_id, review_id)'
            'VALUES (%s, %s, %s)',
            ('Discordo craque.',
             2,
             1)
            )

cur.execute('INSERT INTO reports (message, student_id, review_id)'
            'VALUES (%s, %s, %s)',
            ('Achei paia.',
             3,
             1)
            )

cur.execute('INSERT INTO reports (message, student_id, review_id)'
            'VALUES (%s, %s, %s)',
            ('Tem que tirar da plataforma.',
             3,
             2)
            )

# Create Views

cur.execute('CREATE VIEW CLASS_VIEW AS '
            'SELECT classes.class_id, classes.number, disciplines.discipline_name, professors.professor_name '
            'FROM classes, disciplines, professors '
            'WHERE classes.discipline_id = disciplines.discipline_id AND classes.professor_id = professors.professor_id;'
            )

cur.execute('CREATE VIEW REVIEW_VIEW AS '
            'SELECT reviews.review_id, reviews.class_id, reviews.message, reviews.grade, students.student_name, students.curso '
            'FROM reviews, students '
            'WHERE reviews.student_id = students.student_id;'
            )

conn.commit()

cur.close()
conn.close()