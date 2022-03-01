import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
    r"/\w*(\w)\w*\1\w*/i",
    r"/\w*(\w)\w*(\1\w*){3}/i",
    r"/^(0|1)[01]*\1$|^[01]?$/",
    r"/\b(?=\w*cat)\w{6}\b/i",
    r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
    r"/\b(?!\w*cat)\w{6}\b/i",
    r"/\b(?!\w*(\w)\w*\1)\w+\b/i",
    r"/^(?![10]*10011)[10]*$/",
    r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
    r"/^(?![10]*1(0|1)1)[10]*$/"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Johanna Lohmus p6 2023
