#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("begin")
cursor.execute("delete from results where boats_ref in (select id from boats where name='')")
cursor.execute("delete from boats where name=''")
cursor.execute("rollback")
