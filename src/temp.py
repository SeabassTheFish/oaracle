#!/usr/local/bin/python3

import json


listofRegattas = json.load(open('racesList.txt'))

for regatta in listofRegattas:
    if regatta['Race1'] is not None and len(regatta['Race1']) > 0:
        if regatta['Race1'][0]['IsPublished']:
            print(regatta['Race1'][0]['Id'])
