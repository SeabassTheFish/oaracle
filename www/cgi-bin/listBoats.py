#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json
import cgi
import cgitb
cgitb.enable()

print('Content-Type: application/json') # HTML is following
print()                         # Leave a blank line
connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute('''select name from regattas limit 5''');
try:
    printout = cursor.fetchall()
    for i in range(len(printout)):
        printout[i] = printout[i][0]
except:
    print('<p>We had an oopsie</p>')
    raise SystemExit(1)
print('{"teams": ' + json.dumps(printout) + '}')
