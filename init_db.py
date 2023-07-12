import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS students;')
cur.execute('CREATE TABLE students (id serial PRIMARY KEY,'
                                 'nome varchar (50) NOT NULL,'
                                 'curso varchar (100) NOT NULL,'
                                 'is_admin bit DEFAULT 0,'
                                 'email varchar(150) NOT NULL UNIQUE,'
                                 'password varchar(30) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS departments;')
cur.execute('CREATE TABLE departments (id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
                                 'created_at date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS disciplines;')
cur.execute('CREATE TABLE disciplines (id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
                                 'CONSTRAINT fk_department'
                                    'FOREIGN KEY(department_id)' 
                                    'REFERENCES departments(department_id)'
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