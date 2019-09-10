#!/usr/local/bin/python3

# Made to test my algorithm and figure out if it's predicting stuff right

import psycopg2
import psycopg2.extras
import json
from datetime import datetime
import statistics
from rankTeams import calcDiff

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

def checkAlgorithm(startDatetime, endDatetime, boatsList):
    cursor.execute("select r.id from results r, regattas reg where r.regatta = reg.id and reg.startdate between '{}' and '{}'".format(startDatetime, endDatetime))
    print(cursor.fetchall())

checkAlgorithm("2017-04-08 13:20:00", "2017-08-19 20:35:00", [])
