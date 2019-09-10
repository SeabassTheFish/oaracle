#!/usr/local/bin/python3

import re
import psycopg2
import psycopg2.extras
import json
import requests
from datetime import datetime
from utils import *
from parseRaceName import *


listofRegattas = []
listofResults = {}
formattedRegattas = {}

def dictFromCrsr(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column += 1
    return results

def globalizeList(jsonInput):
    returnDict = {}
    for item in jsonInput:
        returnDict.update(globalizeItem(item))
    return returnDict

def globalizeItem(jsonItem):
    returnDict = {}
    if isinstance(jsonItem, dict):
        for key, value in jsonItem.items():
            if key == "$id":
                returnDict[int(value)] = jsonItem
            if isinstance(value, dict):
                if "$id" in value:
                    returnDict.update(globalizeItem(value))
            if isinstance(value, list):
                for d in value:
                    returnDict.update(globalizeItem(d))
    return returnDict

def getBoatsInRace(jsonInput, referenceDict, raceId):
    boatsList = []
    if isinstance(jsonInput["EntryResults"], list):
        if len(jsonInput["EntryResults"]) > 0:
            if "Entry" in jsonInput["EntryResults"][0] and jsonInput["EntryResults"][0]["Entry"] is not None:
                if "Event" in jsonInput["EntryResults"][0]["Entry"] and jsonInput["EntryResults"][0]["Entry"]["Event"] is not None:
                    if "Entries" in jsonInput["EntryResults"][0]["Entry"]["Event"] and jsonInput["EntryResults"][0]["Entry"]["Event"]["Entries"] is not None:
                        entryList = jsonInput["EntryResults"][0]["Entry"]["Event"]["Entries"]
                        for entry in entryList:
                            if "$ref" in entry:
                                entry = vetRefs(entry, referenceDict)
                            boatsList.append({"name": entry["Name"], "startTime": entry["EntryResults"][0]["StartTime1"], "finishTime": entry["EntryResults"][0]["FinishTime1"], "affiliationName": entry["AffiliationName"], "status": entry["Status"], "race": raceId})
    return boatsList

def vetRefs(jsonInput, referenceDict):
    returnJson = {}
    if "$ref" in jsonInput:
        returnJson = referenceDict[int(jsonInput["$ref"])]
        if "EntryResults" in returnJson:
            for obj in range(len(returnJson["EntryResults"])):
                if "$ref" in returnJson["EntryResults"][obj]:
                    returnJson["EntryResults"][obj] = referenceDict[int(returnJson["EntryResults"][obj]["$ref"])]
    else:
        returnJson = jsonInput         
    return returnJson         

def parseEntryName(name, raceName):
    club = ""
    rower = ""
    weight = ""
    startParen = name.find("(")
    endParen = name.find(")")
    if startParen != -1:
        if raceName.find(" 1x") != -1 or raceName.find(" 2x") != -1:
            club = name[startParen:endParen]
            rower = name[:(startParen - 1)]
        else:
            rower = name[startParen:endParen]
            club = name[:(startParen - 1)]
    return [club, rower]


def parseTime(timeString):
    try:
        return datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S.%f")
    except:
        return datetime.now()

def cmpResults(val):
    return parseTime(val["finishTime"]) - parseTime(val["startTime"])

def processRace(fetched, dbRaceId, dbRegattaId, raceName, connection):
    place = 1
    cursor = connection.cursor()
    for event in sorted(fetched, key=cmpResults):
        rawTime = parseTime(event["finishTime"]) - parseTime(event["startTime"])
        raceNameDict = parseRaceName(raceName)
        boatType = raceNameDict['boatType']
        league = raceNameDict['league']
        weight = raceNameDict['weight']
        gender = raceNameDict['gender']
        name = fixQuote(event['name'])
        (club, rower) = parseEntryName(event["name"], boatType)
        if event['status'] == 'OK':
            dqed = False
        else:
            dqed = True
        cursor.execute('''insert into results (id, boattype, raw_time, place, dqed, race, regatta, gender, weight, league, name, last_update) values (default, \'{}\', \'{}\', {}, {}, {}, {}, \'{}\', \'{}\', \'{}\', \'{}\', now())'''.format(\
               boatType,\
               rawTime,\
               place,\
               dqed,\
               dbRaceId,\
               dbRegattaId,\
               gender,\
               weight,\
               league,\
               name))
        connection.commit()
        place += 1

def populate(connection, regattaIds):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Fetch all regatta info from HereNow
    for temp in regattaIds:
        regattaId = temp[0]
        cursor.execute('''select * from regattas where herenow_id={}'''.format(regattaId))
        fetched = cursor.fetchall()
        regattaColumnDict = dictFromCrsr(cursor)
        link = fetched[0][regattaColumnDict['link']]
        dbId = fetched[0][regattaColumnDict['id']]
        regattaName = fetched[0][regattaColumnDict['name']]
        rawText = json.loads(requests.get(link).text)
        referenceDict = globalizeList(rawText)
        # For each regatta, pull out results
        for event in rawText:
            cursor.execute('''select id, name, herenow_id from races where regatta_id={}'''.format(dbId))
            fetchedDict = {}
            for item in cursor.fetchall():
                fetchedDict[item[2]] = item

            # Making globalized dictionaries 
            if "$ref" in event:
                import pdb
                import pprint
                print("We got to point A")
                try:
                    event = vetRefs(event, referenceDict)
                except:
                    raise
            hereNowId = event["ID"]
            try:
                dbRace = fetchedDict[hereNowId]
            except:
                pass
            boats = getBoatsInRace(event, referenceDict, dbRace[0])
            if len(boats) > 0:
                try:
                    processRace(boats, dbRace[0], dbId, dbRace[1], connection)
                except psycopg2.IntegrityError as e:
                    connection.rollback()
            print("Finished with {}".format(regattaName))

connection = psycopg2.connect("dbname=theoaracle user=sebastian")
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute('''select herenow_id from regattas''')
hereNowIds = cursor.fetchall()
populate(connection, hereNowIds) 
