pymist
=====

> Python port of node's [minimist](github.com/substack/minimist) module

##usage
```Python
from pymist import parse

"""
result: {
    'a': True,
    'b': 1
}
"""
parse(['-a', '-b', '1'])

"""
result: {
    'mode': 'debug',
    'f': 'test.py'
}
"""
parse(['--mode=debug', '-f', 'test.py'])
```
