import re

word = input()
found = re.match(r'the\b', word)
if found is None:
    print(False)
else:
    print(True)
