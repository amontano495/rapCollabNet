import sys
import string

edgeListFile = open('edge_list','r')
rapperFile = open('rapperListUpdated','w')
rapperListFile = open('rapperList','r')

rapperList = list()

for rapper in rapperListFile:
    rapperList.append(str(rapper)[:-1])

tableEntry = list()

for entry in edgeListFile:
    entryList = entry.split(',')
    if entryList[1][:-1] not in rapperList:
        tableEntry.append(str(entryList[1]))

tableEntry = list(set(tableEntry))
rapperFile.writelines(tableEntry)
rapperFile.close()
rapperListFile.close()
edgeListFile.close()
