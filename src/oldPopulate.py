[?1049h[?1h=[1;43r[23m[24m[m[H[J[?25l[43;1HUsing swap file ".populateResults.py.swp"
Original file "~/oaracle/populateResults.py"
Recovery completed. Buffer contents equals file contents.
You may want to delete the .swp file now.

[32mPress ENTER or type command to continue[34h[?25h[m[1;1H[5L[?25l[1;1H[1m[36m#!/usr/local/bin/python3[m

[1m[34mimport[m re
[1m[34mimport[m psycopg2
[1m[34mimport[m psycopg2.extras
[1m[34mimport[m json
[1m[34mimport[m requests
[1m[34mfrom[m datetime [1m[34mimport[m datetime


[1m[36m#cursor.execute('''select * from races where regatta_id=20258''')[m

listofRegattas = []
listofRaces = []
globalDict = {}
listofResults = {}
formattedRegattas = {}

[1m[33mdef[m [1m[36mdictFromCrsr[m(cursor):
    results = {}
    column = [1m[35m0[m
    [1m[33mfor[m d [1m[33min[m cursor.description:[23;9Hresults[d[[1m[35m0[m]] = column[24;9Hcolumn += [1m[35m1[m
    [1m[33mreturn[m results

[1m[33mdef[m [1m[36mfixQuote[m(string):
    returnString = string
    returnString = returnString.replace([1m[35m"'"[m, [1m[35m"''"[m)
    [1m[33mreturn[m returnString

[1m[33mdef[m [1m[36mglobalizeList[m(jsonInput):
    returnList = []
    [1m[33mfor[m item [1m[33min[m jsonInput:[35;9HreturnList.append(globalizeItem(item))
    [1m[33mreturn[m returnList

[1m[33mdef[m [1m[36mglobalizeItem[m(jsonItem):
    returnDict = {}
    [1m[33mif[m [1m[36misinstance[m(jsonItem, [1m[36mdict[m):[41;9H[1m[33mfor[m key, value [1m[33min[m jsonItem.items():
[1m[7m (1) populateResults.py                                                                                               L:1  C:1                 [python] Top  [m[43;1H[K[1;1H[34h[?25h[?25l[43;1H[1m-- INSERT --[1;41r[m[41;1H
[1;43r[41;13H[1m[33mif[m key == [1m[35m"$id"[m:[42;25H[1m[7m[+][1;1H[34h[?25h[?25l[2;41r[m[2;1H[L[1;43r[42;121H[1m[7m2[2;1H[34h[?25h[?25l[3;41r[m[3;1H[L[1;43r[42;121H[1m[7m3[3;1H[34h[?25h[?25l[m[43;1H[K[42;126H[1m[7m0-1[3;1H[34h[?25h[?25l[m[43;1HType  :qa!  and press <Enter> to abandon all changes and exit Vim[3;1H[34h[?25h[?25l[34h[?25h[?25l[1;41r[1;1H[20M[1;43r[22;9H[1m[33mfor[m key, value [1m[33min[m jsonItem.items():[23;13H[1m[33mif[m key == [1m[35m"$id"[m:[24;17HreturnDict[[1m[36mint[m(value)] = jsonItem[25;13H[1m[33mif[m [1m[36misinstance[m(value, [1m[36mdict[m):[26;17H[1m[33mif[m [1m[35m"$id"[m [1m[33min[m value:[27;21HreturnDict[[1m[36mint[m(value[[1m[35m'$id'[m])] = globalizeItem(value)[28;13H[1m[33mif[m [1m[36misinstance[m(value, [1m[36mlist[m):[29;17H[1m[33mfor[m Dict [1m[33min[m value:[30;21HreturnDict[Dict[[1m[35m'$id'[m]] = globalizeItem(Dict)
    [1m[33mreturn[m returnDict

[1m[33mdef[m [1m[36mgetBoatsInRace[m(jsonInput, referenceDict, raceId):
    returnDict = {}
    boatsList = []
    entryList = jsonInput[[1m[35m"EntryResults"[m][[1m[35m0[m][[1m[35m"Entry"[m][[1m[35m"Event"[m][[1m[35m"Entries"[m]
    [1m[33mfor[m entry [1m[33min[m entryList:[38;9Hentry = vetRefs(entry, referenceDict)[39;9HboatsList.append({[1m[35m"name"[m: entry[[1m[35m"Name"[m], [1m[35m"startTime"[m: entry[[1m[35m"EntryResults"[m][[1m[35m0[m][[1m[35m"StartTime1"[m], [1m[35m"finishTime"[m: entry[[1m[35m"EntryResults"[m][[1m[35m0[m][[1m[35m"FinishTime1"[m],  [40;1H[1m[35m"affiliationName"[m: entry[[1m[35m"AffiliationName"[m], [1m[35m"split1"[m: entry[[1m[35m"split1Time"[m], [1m[35m"split2"[m: entry[[1m[35m"split2Time"[m], [1m[35m"split3"[m: entry[[1m[35m"split3Time"[m], [1m[35m"status"[m: entry[[1m[35m"Stt[41;1Hatus"[m], [1m[35m"raceId"[m: entry[[1m[35m"raceId"[m], [1m[35m"race"[m: raceId})[43;1H[K[42;121H[1m[7m23  C:5 [24C14%[3;5H[34h[?25h[23m[24m[m[H[J[?25l[1;5Hresults = {}
    column = [1m[35m0[m
    [1m[33mfor[m d [1m[33min[m cursor.description:[4;9Hresults[d[[1m[35m0[m]] = column[5;9Hcolumn += [1m[35m1[m
    [1m[33mreturn[m results

[1m[33mdef[m [1m[36mfixQuote[m(string):
    returnString = string
    returnString = returnString.replace([1m[35m"'"[m, [1m[35m"''"[m)
    [1m[33mreturn[m returnString

[1m[33mdef[m [1m[36mglobalizeList[m(jsonInput):
    returnList = []
    [1m[33mfor[m item [1m[33min[m jsonInput:[16;9HreturnList.append(globalizeItem(item))
    [1m[33mreturn[m returnList

[1m[33mdef[m [1m[36mglobalizeItem[m(jsonItem):
    returnDict = {}
    [1m[33mif[m [1m[36misinstance[m(jsonItem, [1m[36mdict[m):[22;9H[1m[33mfor[m key, value [1m[33min[m jsonItem.items():[23;13H[1m[33mif[m key == [1m[35m"$id"[m:[24;17HreturnDict[[1m[36mint[m(value)] = jsonItem[25;13H[1m[33mif[m [1m[36misinstance[m(value, [1m[36mdict[m):[26;17H[1m[33mif[m [1m[35m"$id"[m [1m[33min[m value:[27;21HreturnDict[[1m[36mint[m(value[[1m[35m'$id'[m])] = globalizeItem(value)[28;13H[1m[33mif[m [1m[36misinstance[m(value, [1m[36mlist[m):[29;17H[1m[33mfor[m Dict [1m[33min[m value:[30;21HreturnDict[Dict[[1m[35m'$id'[m]] = globalizeItem(Dict)
    [1m[33mreturn[m returnDict

[1m[33mdef[m [1m[36mgetBoatsInRace[m(jsonInput, referenceDict, raceId):
    returnDict = {}
    boatsList = []
    entryList = jsonInput[[1m[35m"EntryResults"[m][[1m[35m0[m][[1m[35m"Entry"[m][[1m[35m"Event"[m][[1m[35m"Entries"[m]
    [1m[33mfor[m entry [1m[33min[m entryList:[38;9Hentry = vetRefs(entry, referenceDict)[39;9HboatsList.append({[1m[35m"name"[m: entry[[1m[35m"Name"[m], [1m[35m"startTime"[m: entry[[1m[35m"EntryResults"[m][[1m[35m0[m][[1m[35m"StartTime1"[m], [1m[35m"finishTime"[m: entry[[1m[35m"EntryResults"[m][[1m[35m0[m][[1m[35m"FinishTime1"[m], [1m[35m"affiliationName"[m: entry[[1m[35m"Affilii[40;1HationName"[m], [1m[35m"split1"[m: entry[[1m[35m"split1Time"[m], [1m[35m"split2"[m: entry[[1m[35m"split2Time"[m], [1m[35m"split3"[m: entry[[1m[35m"split3Time"[m], [1m[35m"status"[m: entry[[1m[35m"Status"[m], [1m[35m"raceId"[m: entry[[1m[35m"raceId"[m], [1m[35m"race"[m: raceId})
    [1m[33mreturn[m boatsList

[1m[33mdef[m [1m[36mvetRefs[m(jsonInput, referenceDict):
    returnJson = {}
    [1m[33mif[m [1m[35m"$ref"[m [1m[33min[m jsonInput:[46;9H[1m[36mprint[m(referenceDict)[47;9HreturnJson = referenceDict[[1m[36mint[m(jsonInput[[1m[35m"$ref"[m])][48;9H[1m[33mif[m [1m[35m"EntryResults"[m [1m[33min[m returnJson:[49;13H[1m[33mfor[m obj [1m[33min[m [1m[36mrange[m([1m[36mlen[m(returnJson[[1m[35m"EntryResults"[m])):[50;17H[1m[33mif[m [1m[35m"$ref"[m [1m[33min[m returnJson[[1m[35m"EntryResults"[m][obj]:[51;21HreturnJson[[1m[35m"EntryResults"[m][obj] = referenceDict[[1m[36mint[m(returnJson[[1m[35m"EntryResults"[m][obj][[1m[35m"$ref"[m])]
[1m[7m (1) populateResults.py [+]                                                                                                                           L:23  C:5                [python] 15%  [3;5H[34h[?25h[?25l[m[53;1H[1mrecording @u[3;5H[34h[?25h[?25l[53;1H-- INSERT --recording @u[3;5H[34h[?25h[?25l[mtfor d [1m[33min[m cursor.description:[52;159H[1m[7m6[3;6H[34h[?25h[53;1H[m[?1l>[?1049lVim: Error reading input, exiting...
Vim: preserving files...
Vim: Finished.
[53;1H[J