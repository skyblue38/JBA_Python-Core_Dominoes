import re

string = input()
regex = r'\$\d+'
match = re.match(regex, string)
if match:
    print('Amount found:', match.group())
else:
    print('No match!')