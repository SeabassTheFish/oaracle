#!/usr/local/bin/python3

# The goal is to add references to the boats table for each result in the db

import psycopg2
import psycopg2.extras
import json
import parseRaceName
import re
import utils

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor()

cursor.execute('''select id, name, boattype, weight, gender, boatrank, league from boats;''')
columnToIndex = {"id": 0, "name": 1, "boattype": 2, "weight": 3, "gender": 4, "boatrank": 5, "league": 6}

boatsList = cursor.fetchall()
i = 0
for boat in boatsList:
    cursor.execute("select id, race from results where name ilike '%{}%' and boattype='{}' and weight='{}' and gender='{}' and league='{}';".format(\
        utils.fixQuote(str(boat[columnToIndex["name"]])),\
        boat[columnToIndex["boattype"]],\
        boat[columnToIndex["weight"]],\
        boat[columnToIndex["gender"]],\
        boat[columnToIndex["league"]]))
    fetched = cursor.fetchall()
    targetedIds = []
    targetedRaces = []

    for item in fetched:
        targetedIds.append(item[0])
        targetedRaces.append(item[1])

    for race in targetedRaces:
        cursor.execute("select name from races where id={};".format(race))
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
    for ID in targetedIds:
        cursor.execute("update results set boats_ref={} where id={};".format(boat[columnToIndex["id"]], ID)) 
    connection.commit()
