import re


def parse(args, bools=[], strings=[], defaults={}):
    result = {"_": []}

    def setArg(key, val):
        value = parseNumber(val) if key not in strings and isNumber(val) else val
        result[key] = value

    i = 0;
    while i < len(args):
        arg = args[i]

        if re.match(r"^--.+=", arg):
            found = re.match(r"^--([^=]+)=(.*)$", arg)
            setArg(found.group(1), found.group(2))
        elif re.match(r"--no-.+", arg):
            key = re.match(r'--no-(.+)', arg).group(1)
            setArg(key, False)
        elif re.match(r"--.+", arg):
            key = re.match(r"--(.+)", arg).group(1)
            next = args[i+1] if i + 1 < len(args) else None

            if not next:
                setArg(key, '' if key in strings else True)
            elif re.match(r'-',next): 
                setArg(key, '' if key in strings else True)
            elif key not in bools:
                setArg(key, next)
                i = i + 1
            elif re.search('^(true|false)$', next):
                setArg(key, next == 'true')
                i = i + 1
            else:
                setArg(key, True)
        elif re.match("^-[^-]+", arg):
            letters = arg[1:-1]
            broken = False
            k = 0
            while k < len(letters):
                next = arg[k+2:]
                if next == '-':
                    setArg(letters[k], next)
                    k = k + 1
                    continue

                if re.match(r"[A-Za-z]", letters[k]) and \
                    re.match(r"^-?\d+(\.\d+)?(e-?\d+)?$", next):
                    setArg(letters[k], next)
                    broken = True
                    break

                if k + 1 < len(letters) and re.match(r"\W", letters[k+1]):
                    setArg(letters[k], next)
                    broken = True
                    break;

                setArg(letters[k], '' if letters[k] in strings else True)

                k = k + 1

            key = arg[-1]
            if not broken and key != '-':
                if i + 1 < len(args) \
                    and not re.search(r"^(-|--)", args[i+1]) \
                    and key not in bools:
                    setArg(key, args[i+1])
                    i = i + 1
                elif i + 1 < len(args) \
                    and re.search(r'^(true|false)$', args[i+1]):
                    setArg(key, args[i+1] == 'true')
                    i = i + 1
                else:
                    setArg(key, '' if key in strings else True)
        else:
            result["_"].append(parseNumber(arg) if isNumber(arg) else arg)

        i = i + 1

    for key in defaults:
        if key not in result:
            setArg(key, defaults[key])

    return result


def isNumber(n):
    return isInteger(n) or isFloat(n)


def isInteger(n):
    try:
        int(n)
        return True
    except Exception as e:
        return False


def isFloat(n):
    try:
        float(n)
        return True
    except Exception as e:
        return False


def parseNumber(n):
    return int(n) if isInteger(n) else float(n)
