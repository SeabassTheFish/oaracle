#!/usr/local/bin/python3

# Trying to extract the name of each regatta and generate a link

import requests
import json
from datetime import datetime
from datetime import timedelta

r = requests.get("https://api.herenow.com/breeze/BreezeApi/Races")
data = r.text

jsonData = json.loads(data)

#for race in jsonData:
#    try:
#        if race["IsListed"]:
#            print(str(race["Name"]))
#    except:
#        pass

for raceIndex in range(len(jsonData)):
    try:
        if not jsonData[raceIndex]["Id"]:
            del jsonData[raceIndex]
    except:
        pass

def makeLink(race):
    r = None
    if "Id" in race:
        if race["Race1"] != []:
            if "Id" in race["Race1"][0]:
                r = race["Race1"][0]
        else:
            if "Id" in race:
                r = race
    if r is not None:
        return "'https://api.herenow.com/breeze/BreezeApi/GetScopedRaceFlights?raceId=" + str(r["Id"]) + "&scopeStartTime=" + str(r["StartDate"]) + "Z&scopeEndTime=2023-1-1T00:00:00.000Z'"
    else:
        return None


for race in jsonData:
    makeLink(race)


def makeLinkById(race_id):
    for race in jsonData:
        if "Id" in race and race["Id"] == race_id:
            makeLink(race)

makeLinkById(20554)
