#!/usr/local/bin/python3

import psycopg2
import psycopg2.extras
import json
import requests
import time
import argparse
from utils import *

parser = argparse.ArgumentParser(description='Populates races table using race pages on HereNow')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose boi')
args = parser.parse_args()

def populateRaces(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    grabRegattas = cursor.execute("""select herenow_id, name, link, id from regattas where link is not null;""")
    listofRegattas = cursor.fetchall()
    listofRaces = []


    for regatta in listofRegattas:
        listofRaces = json.loads(requests.get(regatta[2]).text)
        time.sleep(1)
        grabRegatta = cursor.execute("""select name from races where regatta_id=%d""" % regatta[3])
        whatWeHave = [x[0] for x in cursor.fetchall()]
        for race in listofRaces:
            try:
                sqlCommand = """insert into races values (default, \'{}\', \'{}\', {}, {}, now());""".format(fixQuote(race['Name']), fixQuote(race['StartTime']), regatta[3], race['ID'])
                print(sqlCommand)
                if race['Name'] not in whatWeHave:
                    cursor.execute(sqlCommand)
                    if args.verbose:
                        print(sqlCommand)
                else:
                    if args.verbose:
                        print("{} in {} is a dupe".format(race['Name'], regatta[0]))
                connection.commit()
            except Exception as exception:
                print(exception)
        

        if args.verbose:
            print("Finished with %s, moving on..." % str(regatta[1]))
            print("Printed {} races".format(len(listofRaces)))

    if args.verbose:
        print("Population complete!")

    cursor.close()
    
connection = psycopg2.connect("dbname=theoaracle user=sebastian")
populateRaces(connection)
