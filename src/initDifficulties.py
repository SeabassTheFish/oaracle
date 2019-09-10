#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute('''select * from boats''')

fetched = cursor.fetchall()

for boat in fetched:
    cursor.execute('''insert into difficulties (id, difficulty, datecalced, boats_ref) values (default, 5, date '1970-01-01', {})'''.format(boat[0]))

connection.commit()
