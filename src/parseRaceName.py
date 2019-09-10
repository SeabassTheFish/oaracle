#!/usr/local/bin/python3

import re

testStrings = ["Men's Lightweight 2x", "Junior Womens Varsity Double", "Lightweight mens novice 8+", "Open women's 4+"]
def parseRaceName(name):
    outputDict = {'boatType': '8+'}
    brokenName = name.split(" ")
    re.I = True
    for s in brokenName:
        if re.fullmatch(r"[1248][-+x]?", s):
            if len(s) == 2:
                outputDict['boatType'] = s
            else:
                outputDict['boatType'] = s + "+"
        
        elif re.match(r"[Mm][ae]n'?'?s?", s):
            outputDict['gender'] = 'M'
        elif re.match(r"[Ww]om[ae]n'?'?s?", s):
            outputDict['gender'] = 'W'
        elif re.match(r"[Bb]oy'?'?s?", s):
            outputDict['gender'] = 'M'
        elif re.match(r"[Gg]irl'?'?s?", s):
            outputDict['gender'] = 'W'

        elif re.match(r"[Oo]pen", s):
            outputDict['weight'] = 'O'
        elif re.match(r"(ltwt|light)", s.lower()):
            outputDict['weight'] = 'L'

        elif re.match(r"[Vv]arsity", s):
            outputDict['league'] = 'V'
        elif re.match(r"[Ee]xper", s):
            outputDict['league'] = 'E'
        elif re.match(r"[Nn]ovice", s):
            outputDict['league'] = 'N'
        elif re.match(r"[Mm]aster", s):
            outputDict['league'] = 'M'
        elif re.match(r"[Cc]ox", s):
            outputDict['league'] = 'C'
        elif re.match(r"[Vv]eteran", s):
            outputDict['league'] = 'T'
        elif re.match(r"[Aa]lum", s):
            outputDict['league'] = 'A'

        elif re.match(r"[Dd]ouble", s):
            outputDict['boatType'] = '2x'
        elif re.match(r"[Pp]air", s):
            outputDict['boatType'] = '2-'
        elif re.match(r"[Ff]our", s):
            outputDict['boatType'] = '4+'
        elif re.match(r"[Qq]uad", s):
            outputDict['boatType'] = '4x'
        elif re.match(r"[Ee]ight", s):
            outputDict['boatType'] = '8+'

        if 'gender' not in outputDict:
            outputDict['gender'] = 'A'
        if 'weight' not in outputDict:
            if 'league' in outputDict and 'league' == 'V':
                outputDict['weight'] = 'H'
            else:
                outputDict['weight'] = 'O'
        if 'league' not in outputDict:
            outputDict['league'] = 'V'

    return outputDict
