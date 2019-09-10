#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json
from datetime import datetime 
import statistics

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

raceId = 62821
cursor.execute('''select * from results where race={} order by place'''.format(raceId))
fetched = cursor.fetchall()

def oldCalcDiff(resultId):
    cursor.execute('''select * from results where id={}'''.format(resultId))
    focalResult = cursor.fetchall()[0]
    if focalResult[9] is None:
        return ("That result had no time")
    race = focalResult[3]
    place = focalResult[2]
    cursor.execute('''select * from results where race={} and raw_time is not null order by place'''.format(race))
    boatsInRace = cursor.fetchall()
    focalTime = datetime.strptime(boatsInRace[focalResult[2] - 1][9], "%H:%M:%S.%f")
    topTime = datetime.strptime(boatsInRace[0][9], "%H:%M:%S.%f")
    bottomTime = datetime.strptime(boatsInRace[-1][9], "%H:%M:%S.%f")
    spread = bottomTime - topTime
    
    # Calculating where the boat stands in comparison to the raw times of other boats
    bracketLength = spread/10
    bracket = 0
    for i in range(10):
        if focalTime < (topTime + i*bracketLength):
            bracket = i
            break
        if i == 9:
            bracket = 10

    # Calculating the average difficulty of the competitors that the boat beat
    loserDiffs = []
    for boat in boatsInRace:
        boatTime = datetime.strptime(boat[9], "%H:%M:%S.%f")
        if focalTime < boatTime:
            cursor.execute('''select id from boats where id={}'''.format(boat[12]))
            boatsId = cursor.fetchall()[0][0]
            cursor.execute('''select difficulty from difficulties where boats_ref={}'''.format(boatsId))
            difficulty = cursor.fetchall()[0][0]
            loserDiffs.append(difficulty)
    if len(loserDiffs) == 0:
        print(10)
    else:
        averageLoserDiff = statistics.mean(loserDiffs)
        testTuple = (averageLoserDiff, len(loserDiffs))
        print(statistics.mean(testTuple))


    score = bracket
    return score

def calcDiff(resultId):
    cursor.execute('''select * from results where id={}'''.format(resultId))
    focalResult = cursor.fetchall()[0]
    race = focalResult[3]
    if focalResult[9] is None:
        return None
    
    cursor.execute('''select b.id from boats b, results r where r.race={} and r.raw_time is not null and b.id=r.boats_ref order by b.id'''.format(race))
    print(cursor.fetchall())

calcDiff(504592)
