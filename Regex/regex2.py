import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
    r"/^[x.o]{64}$/i",
    r"/^[xo]*\.[xo]*$/i",
    r"/^(x*o*\.x*o*|x*o*\.x*o*)$/i",
    r"/^.(..)*$/s",
    r"/^(0([01][01])*|1[01]([01][01])*)$/",
    r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i",
    r"/^(0|10)*1*$/",
    r"/^(\b[bc]*a?[bc]*|[abc])$/",
    r"/^(\b[bc]*((a[bc]*){2}a[bc]*)*[bc]*|[bc])$/",
    r"/^1[02]*1[02]*(1[02]*1[02])*$/"
]

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Johanna Lohmus p6 2023
