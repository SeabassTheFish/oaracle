#!usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json
import requests
from datetime import datetime

connection = psycopg2.connect("dbname=theoaracle user=sebastian")

cursor = connection.cursor()

cursor.execute('''delete * from regattas''')

name = ""
startDate = ""
endDate = ""
location = ""
regatta_Id = 0

listofRegattas = json.loads(requests.get("https://api.herenow.com/breeze/BreezeApi/Races").text)
regattaIdList = []
def fixQuote(string):
    return string.replace("'", "''")

def dictFromCursor(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column += 1
    return results



with connection as psycopg2.connect("dbname=theoaracle user=sebastian"):
    with cursor as connection.cursor:
        # Regatta Portion
        for regatta in listofRegattas:
            if "IsTest" in regatta and regatta["IsTest"]:
                del regatta
                continue
            if "Race1" in regatta and regatta["Race1"] != []:
                listofRegattas.append(regatta["Race2"]
                regatta = regatta["Race1"]
            if "Name" in regatta and regatta["Name"] != "":
                name = regatta["Name"]
            if "StartDate" in regatta and regatta["StartDate"] != "":
                startDate = regatta["StartDate"]
            if "EndDate" in regatta and regatta["EndDate"] != "":
                endDate = regatta["EndDate"]
            if "Subtitle" in regatta and regatta["Subtitle"] != None:
                location = regatta["Subtitle"]
            if "Id" in regatta:
                regatta_Id = regatta["Id"]
            submitLink = makeLink(regatta)
            sql_command = """insert into regattas values (default, {}, {}, {}, {}, {}, {});""".format(fixQuote(name), fixQuote(startDate), fixQuote(endDate), fixQuote(location), regatta_Id, submitLink)
            regattaIdList.append(int(regatta_Id))
            cursor.execute(sql_command)
            
            # Races Portion
            listofRaces = json.loads(requests.get(regatta[6]).text)
            grabRegatta = cursor.execute("""select name from races where regatta_id={}""".format(regatta_Id))
            whatWeHave = [x['name'] for x in cursor.fetchall()]
            for race in listofRaces:
                try:
                    sqlCommand = """insert into races values (default, {}, {}, {});""".format(fixQuote(race['Name']), fixQuote(race['StartTime']), regatta['id'])
                    if race['Name'] not in whatWeHave:
                        cursor.execute(sqlCommand)
                except Exception as exception:
                    print("There was a problem with a race in {}.".format(str(regatta[1])))
                    print("    {} because of {}".format(str(exception), sqlCommand))
                    print(race)


            # Results Portion

            time.sleep(1)

def globalizeList(jsonInput, depositDict):
    for item in jsonInput:
        globalizeItem(item, depositDict)

def globalizeItem(jsonItem, depositDict):
    if isinstance(jsonItem, dict):
        for key, value in jsonItem.items():
            if key == "$id":
                depositDict[int(value)] = jsonItem
            if isinstance(value, dict):
                if "$id" in value:
                    globalizeItem(value, depositDict)
            if isinstance(value, list):
                globalizeList(value, depositDict)

def fetchInfo(jsonInput, referenceDict):
    returnDict = {}
    boatsList = []
    entryList = jsonInput["EntryResults"][0]["Entry"]["Event"]["Entries"]
    for entry in entryList:
        entry = vetRefs(entry, referenceDict)
        boatsList.append({"name": entry["Name"], "startTime": entry["EntryResults"][0]["StartTime1"], "finishTime": entry["EntryResults"][0]["FinishTime1"], "affiliationName": entry["AffiliationName"], "split1": entry["split1Time"], "split2": entry["split2Time"], "split3": entry["split3Time"], "status": entry["Status"], "raceId": entry["raceId"]})
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
    startPeren = name.find("(")
    endPeren = name.find(")")
    if startPeren != -1:
        if raceName.find(" 1x") != -1 or raceName.find(" 2x") != -1:
            club = name[startPeren:endPeren]
            rower = name[:(startPeren - 1)]
        else:
            rower = name[startPeren:endPeren]
            club = name[:(startPeren - 1)]
    return [club, rower]

def parseRaceName(name):
    acceptableNames = ["1x", "2x", "4x", "2-", "2+", "4-", "4+", "8-", "8+"]
    boatType = ""
    weight = ""
    gender = ""
    age = ""
    league = ""
    for acceptName in acceptableNames:
        if acceptName in name:
            boatType = acceptName
    if name.toLowerCase().find("ltwt") != -1 or name.toLowerCase().find("lightweight") != -1 or name.toLowerCase().find("light") != -1:
        weight = "Light"
    elif name.toLowerCase().find("open") != -1:
        weight = "Open"

    if name.toLowerCase().find("men's") != -1:
        gender = "M"
    elif name.toLowerCase().find("women's") != -1:
        gender = "F"
    
    if name.toLowerCase().find("jr") != -1 or name.toLowerCase().find("junior") != -1 or name.toLowerCase().find("youth") != -1:
        age = "jr"
    elif name.toLowerCase().find("master") != -1:
        age = "master"
    elif name.toLowerCase().find("college") != -1:
        age = "college"
    if name.toLowerCase().find("alum") != -1:
        age = "alum"

    if name.toLowerCase.find("novice") != -1:
        league = "novice"
    elif name.toLowerCase.find("championship") != -1:
        league = "champ"
    
        
    return [boatType, weight, gender, age, league]

def parseTime(timeString):
    return datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S")

def populate(regattaIds):
    regattaDict = {}
    with connection as psycopg2.connect("dbname=theoaracle user=sebastian"):
        with cursor as connection.cursor(cursor_factory=psycopg2.extras.DictCursor):
            for regattaId in regattaIds:
                cursor.execute('''select * from regattas where id={}'''.format(regattaId))
                regattaDict.update({regattaId: cursor.fetchall()})
            for key, value in regattaDict.items():
                cursor.execute('''select id from races where regatta_id={}'''.format(key))
                raceIdList = [ID for ID in cursor.fetchall()]
                referenceDict = {}
                globalizeList(value, referenceDict)
                fetched = [fetchInfo(race, referenceDict) for race in value]
            for event in fetched:
                rawTime = parseTime(event["finishTime"] - parseTime(event["startTime"])
                query = '''insert into results values (default, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'''.format(parseRaceName(value["Name"])[0], parseEntryName(event["name"], parseRaceName(value["Name"])[0])[0], parseEntryName(event["name"], parseRaceName(value["Name"])[0])[1], rawTime, event["split1"], event["split2"], event["split3"], calculatePlace(#TODO), event["Status"], race, key, parseRaceName(value["Name"])[2], parseRaceName(value["Name"])[1]}

            columnDict = dictFromCrsr(cursor)
            print(columnDict)

def calculatePlace(eventEntries, boatIndex):
    place = 1
    netTime = parseTime(eventEntries[boatIndex]["FinishTime1"]) - parseTime(eventEntries[boatIndex]["StartTime1"])
    for boat in eventEntries:
        if boat["FinishTime1"] - boat["StartTime1"] < netTime:
            place += 1
    return place
        
for regatta in listofRegattas:
    listofRaces = json.loads(requests.get(regatta[columnDict['link']]).text)
        print(listofRaces)
        globalizeList(listofRaces, globalDict)
        for race in listofRaces:
            pass

