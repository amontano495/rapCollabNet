import sys
import string

rapperListFile = open('rapperList','r')
idCSV = open('idTable.csv','w')

tableEntry = list()

i = 0

for rapper in rapperListFile:
    tableEntry.append(str(str(i) + ',' + rapper))
    i = i + 1

idCSV.writelines(tableEntry)
idCSV.close()
rapperListFile.close()
