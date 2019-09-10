#!/usr/local/bin/python3

def parseName(name, raceName):
    club = ""
    rower = ""
    weight = ""
    startParen = name.find("(")
    endParen = name.find(")")
    if startParen != -1:
        if raceName.find("1x") != -1 or raceName.find("2x") != -1 or raceName.find("2-") != -1:
            club = name[startParen+1:endParen]
            rower = name[:(startParen - 1)]
        else:
            rower = name[startParen+1:endParen]
            club = name[:(startParen - 1)]
    return [club, rower]

def fixQuote(string):
    return string.replace("'", "''")

