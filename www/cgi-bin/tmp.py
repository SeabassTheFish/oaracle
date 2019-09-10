#!/usr/local/bin/python3

import json
import cgi
import cgitb
import psycopg2
cgitb.enable()

print('Content-Type: application/json') # HTML is following
print()                         # Leave a blank line
print('{teams: ["whatever", "hi"]}')
