import sys
import re

'''
line = '/wiki/Drake_(rapper)"'
matchObj = re.search(r'(/wiki/)(([a-zA-Z0-9!@#$%^&_ ])*)([(])',line)
if  matchObj:
    print matchObj.group(2)

'''
file = open('artistshtml','r')

for line in file:
    try:
        matchObj = re.search(r'(</span><span>)(([a-zA-Z0-9!@#$%^&_ ]|[.])+)(</span><span>)',line)
        print matchObj.group(2)
    except:
        pass
