#!/usr/local/bin/python3

import psycopg2

connection = psycopg2.connect("dbname=theoaracle user=sebastian")

crsr = connection.cursor()

sql_command = "insert into rowers values (default, 'Sebastian', 'Neumann', 15, False, 'M', Null)"

crsr.execute(sql_command)

connection.commit()

crsr.close()
connection.close()
