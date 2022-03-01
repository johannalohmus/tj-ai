import sys; args = sys.argv[1:]
idx = int(args[0])-70

myRegexLst = [
    r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)[a-z]+$/m",
    r"/^(?!(.*[aeiou]){6})([a-z]*[aeiou][a-z]*){5}$/m",
    r"/^(?=.*[^aeiou\n]w[^aeiou]{2})[a-z]*$/m",
    r"/^((?=(.)(.)(.))[a-z]*(?=\4\3\2$)[a-z]*|aa?)$/m",
    r"/^[^btA-Z\n']*(bt|tb)[^btA-Z\n']*$/m",
    r"/^(?=.*(.)\1)[a-z]*$/m",
    r"/^(?=.*(.)(.*\1){5})[a-z]*$/m",
    r"/^(?=.*((.)\2){3})[a-z]*$/m",
    r"/^(?=(.*[^aeiou\n]){13})[a-z]*$/m",
    r"/^(?!.*(.)(.*\1){2})+[a-z]+$/m"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Johanna Lohmus p6 2023
