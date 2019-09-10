#!/usr/local/bin/python3

import cgi
import cgitb
cgitb.enable()
    
input_data = cgi.FieldStorage()

print('Content-Type:text/html') # HTML is following
print()                         # Leave a blank line
print('<h1>Addition Results</h1>')
