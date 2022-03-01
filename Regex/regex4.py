import sys; args = sys.argv[1:]
idx = int(args[0])-60

myRegexLst = [
    r"/^(?!.*010)[01]*$/",
    r"/^(?!.*101)(?!.*010)[01]*$/",
    r"/^([01])[01]*(\1)$|^[01]?$/",
    r"/\b(?!\w*(\w)\w*\1\b)\w+\b/i",
    r"/\b\w*(\w)\w*(?=\w*\1)\w*(\w)\w*(?!\w*\1)(?=\w*\2)\w*\b/i",
    r"//",
    r"//",
    r"//",
    r"/^(?!0\d)(0|1(01*0)*1)+$/",
    r"/^(?!0\d)(1|01*0)+$/"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Johanna Lohmus p6 2023
