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
                                 'nome varchar (50) NOT NULL,'
                                 'curso varchar (100) NOT NULL,'
                                 "is_admin bit DEFAULT '0',"
                                 'email varchar(150) NOT NULL UNIQUE,'
                                 'password varchar(30) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS departments;')
cur.execute('CREATE TABLE departments (department_id serial PRIMARY KEY,'
                                 'codigo INT NOT NULL UNIQUE,'
                                 'nome varchar (150) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

with open('./ofertas_sigaa/data/2023.1/departamentos_2023-1.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            sql = "INSERT INTO departments (codigo, nome) VALUES (" + row[0] + " , '" + row[1] + "');"
            cur.execute(sql)

cur.execute('DROP TABLE IF EXISTS disciplines;')
cur.execute('CREATE TABLE disciplines (discipline_id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
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
            sql = "INSERT INTO disciplines (codigo, nome, department_id) VALUES ('"+ row[0] + "' , '" + row[1] + "', (SELECT department_id FROM departments WHERE codigo = " + row[2] + "));"
            cur.execute(sql)

cur.execute('DROP TABLE IF EXISTS professors;')
cur.execute('CREATE TABLE professors (professor_id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
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
                sql = "INSERT INTO professors (nome, department_id) VALUES ('"+ row[2] + "' , (SELECT department_id FROM departments WHERE codigo = " + row[8] + "))"
                cur.execute(sql)
                professores_adicionados.append(row[2])
            sql = "INSERT INTO classes (number, discipline_id, professor_id) VALUES ('"+ row[0] + "' , (SELECT discipline_id FROM disciplines WHERE codigo = '" + row[7] + "' LIMIT 1), (SELECT professor_id FROM professors WHERE nome = '" + row[2] + "' LIMIT 1));"
            cur.execute(sql)
            line_count += 1

cur.execute('DROP TABLE IF EXISTS reviews;')
cur.execute('CREATE TABLE reviews (review_id serial PRIMARY KEY,'
                                 'message text NOT NULL,'
                                 'student_id INT NOT NULL,'
                                 'professor_id INT NOT NULL,'
                                 'department_id INT NOT NULL,'
                                 'CONSTRAINT fk_student '
                                    'FOREIGN KEY(student_id)' 
                                    'REFERENCES students(student_id),'
                                 'CONSTRAINT fk_professor '
                                    'FOREIGN KEY(professor_id)' 
                                    'REFERENCES professors(professor_id),'
                                 'CONSTRAINT fk_department '
                                    'FOREIGN KEY(department_id)' 
                                    'REFERENCES departments(department_id),'
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

# Execute a command: this creates a new table
# cur.execute('DROP TABLE IF EXISTS books;')
# cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
#                                  'title varchar (150) NOT NULL,'
#                                  'author varchar (50) NOT NULL,'
#                                  'pages_num integer NOT NULL,'
#                                  'review text,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP);'
#                                  )

# # Insert data into the table

# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('A Tale of Two Cities',
#              'Charles Dickens',
#              489,
#              'A great classic!')
#             )


# cur.execute('INSERT INTO books (title, author, pages_num, review)'
#             'VALUES (%s, %s, %s, %s)',
#             ('Anna Karenina',
#              'Leo Tolstoy',
#              864,
#              'Another great classic!')
#             )

conn.commit()

cur.close()
conn.close()