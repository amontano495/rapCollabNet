import sys
import string

rapperEdgeFile = open('edge_list','r')
idCSV = open('idTable.csv','r')
edgeCSV = open('edgeTable.csv','w')

idTable = list()

for entry in idCSV:
    idTable.append(entry)

def getID(rapName,idTable):
    for entry in idTable:
        if rapName == entry.split(',')[1][:-1]:
            return entry.split(',')[0]

tableEntry = list()

for edge in rapperEdgeFile:
    edgeList = edge.split(',')
    src = getID(edgeList[0],idTable)
    dest = getID(edgeList[1][:-1],idTable)
    if src != None and dest != None:
        tableEntry.append(str(src + ',' + dest + '\n'))
    else:
        continue

edgeCSV.writelines(tableEntry)

edgeCSV.close()
rapperEdgeFile.close()
idCSV.close()

