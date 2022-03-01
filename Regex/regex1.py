import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
    r"/^0$|^10[10]$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^1[01]*0$|^0$/",
    r"/^[01]*110[01]*$/",
    r"/^...?.?$/s",
    r"/^\d{3}*-?*\d\d*-?*\d{4}$/",
    r"/^[^d\n]*d\w*/im",
    r"/^1[01]*1$|^0[01]*0$|^[01]?$/"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Johanna Lohmus p6 2023
