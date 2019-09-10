#!/usr/local/bin/python3

import psycopg2
import json
import requests
from testGrab import makeLink
import argparse
import sys
from utils import *

hereNowUrl = "https://api.herenow.com/breeze/BreezeApi/Races"

parser = argparse.ArgumentParser(description='Populates Regattas table using top level HereNow')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose boi')
parser.add_argument('-f', dest='filename', action='store', help='filename to use instead of HereNow')
parser.add_argument('-t', dest='trunc', action='store_true', help='truncate that madlad')
args = parser.parse_args()

def recurInto(regatta, fieldname, cursor, currentIds):
    if fieldname in regatta and regatta[fieldname] is not None:
        if isinstance(regatta[fieldname], dict):
            interpretRegatta(regatta[fieldname], cursor, currentIds)
        if isinstance(regatta[fieldname], list):
            for r in regatta[fieldname]:
                interpretRegatta(r, cursor, currentIds)

def interpretRegatta(regatta, cursor, currentIds):
    name = ""
    startDate = ""
    endDate = ""
    subtitle = ""
    if not isinstance(regatta, dict) or "Id" not in regatta:
        return
    regatta_Id = regatta["Id"]
    if regatta_Id in currentIds:
        if args.verbose:
            print("Already got this one, chief: {}".format(regatta_Id))
        return
    if "IsTest" in regatta and regatta["IsTest"]:
        return
    if "IsListed" in regatta and not regatta["IsListed"]:
        return
    recurInto(regatta, "Race1", cursor, currentIds)
    recurInto(regatta, "Race2", cursor, currentIds)
    if "Name" in regatta and len(regatta["Name"]) != 0:
        name = regatta["Name"]
    if "StartDate" in regatta and len(regatta["StartDate"]) != 0:
        startDate = regatta["StartDate"]
    if "EndDate" in regatta and len(regatta["EndDate"]) != 0:
        endDate = regatta["EndDate"]
    if "Subtitle" in regatta and regatta["Subtitle"] != None and len(regatta["Subtitle"]) != 0:
        subtitle = regatta["Subtitle"]
    submitLink = makeLink(regatta)
    if submitLink is not None:
        sql_command = """insert into regattas values (default, \'%s\', \'%s\', \'%s\', \'%s\', \'%d\', %s, false, now());""" % (fixQuote(name), fixQuote(startDate), fixQuote(endDate), fixQuote(subtitle), regatta_Id, submitLink)
        if args.verbose:
            print(sql_command)
        cursor.execute(sql_command)
    else:
        print("Someone did an oopsie: {}".format(regatta_Id), file=sys.stderr)

def populateRegattas(connection):
    cursor = connection.cursor()
    if args.trunc:
        cursor.execute("delete from regattas")
    cursor.execute("select hereNow_id from regattas;")
    currentIds = [x[0] for x in cursor.fetchall()]
    
    if args.filename is not None:
        listofRegattas = json.load(open(args.filename))
    else:
        listofRegattas = json.loads(requests.get(hereNowUrl).text)

    for regatta in listofRegattas:
        interpretRegatta(regatta, cursor, currentIds)

    connection.commit()

    cursor.close()

populateRegattas(psycopg2.connect("dbname=theoaracle user=sebastian"))
