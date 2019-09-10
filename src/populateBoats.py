#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json
from utils import *
import re

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


# New Stuff
cursor.execute('''select name, boattype, weight, gender, race, league from results''')
fetched = cursor.fetchall()
newBoatsSet = set()
for item in fetched:
    opName = item[0]
    opBoatType = item[1]
    opWeight = item[2]
    opGender = item[3]
    opRace = item[4]
    opLeague = item[5]

    cursor.execute("select name from races where id={}".format(opRace))
    raceName = cursor.fetchall()[0][0]

    boatRank = 1
    if re.match(r"[Ss]econd", raceName):
        boatRank = 2
    elif re.match(r"[Tt]hird", raceName):
        boatRank = 3
    elif re.match(r"[Ff]ourth", raceName):
        boatRank = 4
    elif re.match(r"[Ff]ifth", raceName):
        boatRank = 5
    else:
        m = re.search(r"([2345])[VvNn]", raceName)
        if m:
            boatRank = int(m.group(1))

    (club, rower) = parseName(opName, opBoatType)
    boatName = club
    splitted = club.split(" ")
    if len(splitted[-1]) == 1:
        boatRank = ord(splitted[-1]) - 64
        boatName = " ".join(splitted[:-1])
    newBoatsSet.add((boatName, boatRank, opBoatType, opWeight, opGender, opLeague))

# Old Stuff
cursor.execute('''select name, boatRank, boattype, weight, gender, league from boats''')
currentBoats = cursor.fetchall()
oldBoatsSet = set()
for boat in currentBoats:
    oldBoatsSet.add((boat[0], boat[1], boat[2], boat[3], boat[4], boat[5]))

# Adding unique new stuff to db
for boat in newBoatsSet.difference(oldBoatsSet):
    try:
        sqlCommand = '''insert into boats (id, name, location, boatrank, boattype, weight, gender, league, last_update) values (default, \'{}\', \'{}\', {}, \'{}\', \'{}\', \'{}\', \'{}\', now())'''.format(fixQuote(boat[0]), None, boat[1], fixQuote(boat[2]), fixQuote(boat[3]), fixQuote(boat[4]), fixQuote(boat[5]))
        cursor.execute(sqlCommand)
        connection.commit()
    except UnicodeEncodeError as e:
        connection.rollback()
                
