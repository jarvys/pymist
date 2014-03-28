import sys
import re

def parse(args, bools={}, strings={}, defaults={}):
    result = {"_": None}
    notFlags = None
    if "--" in args:
        notFlags = args[args.index("--")+1:]
        args = args[0:args.index("--")]

    def setArg(key, val):
        value = parseNumber(val) if key not in strings and isNumber(val) else val
        result[key] = value

    i = 0;
    while i < len(args):
        arg = args[i]

        if re.match(r"^--.+=", arg):
            found = re.match(r"^--([^=]+)=(.*)$", arg)
            setArg(found.group(1), found.group(2))
        else if re.match(r"^--no-.+", arg"):
            key = re.match(r"^--no-(.+)", arg).group(1)
            setArg(key, false)
        else if re.match(r"^--.+", arg):
            key = re.match(r"^--(.+)", arg).group(1)
            next = args[i+1] if i + 1 < len(args) else None

            if not next:
                setArg(key, '' if key in strings else True)
                continue

            if re.match("^-", next):
                setArg(key, '' if key in strings else True)
                continue

            if key in bools:
                setArg(key, True)
                continue

            setArg(key, next)
            i++
        else if re.match("^-[^-]+", arg):
            letters = arg[1:-1])
        else:
            result["_"].append(parseNumber(arg) if isNumber(arg) else arg)

    for key in defaults:
        if key not in result:
            setArg(key, defaults[key])

    return result


def isNumber(n):
    // TODO


def parseNumber(n):
    // TODO


sys.modules[__name__] = parse
