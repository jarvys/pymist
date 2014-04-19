# coding: utf-8
import sys
import unittest

from pymist import parse
from pymist import isInteger, isFloat, isNumber, parseNumber


class TestPymist(unittest.TestCase):

    def test_double_dash(self):
        # cmd --arg
        self.assertEqual(parse(['--arg']), {'arg': True, '_': []})
        # cmd --arg   # arg in strings
        self.assertEqual(parse(['--arg'], strings=['arg']), {'arg': '', '_': []})

        # cmd --arg 1
        self.assertEqual(parse(['--arg', '1']), {'arg': 1, '_': []})
        # cmd --arg 1 # arg in bools
        self.assertEqual(parse(['--arg', '1'], bools = ['arg']), 
                                {'arg': True, '_': [1]})
        # cmd --arg true # arg in bools
        self.assertEqual(parse(['--arg', 'true'], bools = ['arg']), 
                                {'arg': True, '_': []})
        # cmd --arg -b
        self.assertEqual(parse(['--arg', '-b']), {'arg': True, 'b': True, '_': []})
        

        # cmd --arg=1
        self.assertEqual(parse(['--arg=1']), {'arg': 1, '_': []})
        # cmd --arg1 --arg2
        self.assertEqual(parse(['--arg1', '--arg2']), {
            'arg1': True, 
            'arg2': True, 
            '_': []
        })

    def test_single_dash(self):
        # cmd -a
        self.assertEqual(parse(['-a']), {'a': True, '_': []})
        # cmd -a1.24
        self.assertEqual(parse(['-a1.24']), {'a': 1.24, '_': []})
        # cmd -ab1
        self.assertEqual(parse(['-ab1']), {'a': True, 'b': 1, '_': []})
        # cmd -a码农
        self.assertEqual(parse([u'-a码农']), {'a': u'码农', '_': []})
        # cmd -ab
        self.assertEqual(parse(['-ab']), {'a': True, 'b': True, '_': []})
        # cmd -af test.py
        self.assertEqual(parse(['-af', 'test.py']), 
                         {'a': True, 'f': 'test.py', '_': []})
        # cmd -af false  # f in bools
        self.assertEqual(parse(['-af', 'false'], bools=['f']), 
                         {'a': True, 'f': False, '_': []})
        # cmd -af -b  # f in bools
        self.assertEqual(parse(['-af', '-b']), 
                         {'a': True, 'f': True, 'b': True, '_': []})

    def test_left_args(self):
        # cmd a b
        self.assertEqual(parse(['a', 'b']), {'_': ['a', 'b']})
        # cmd -a b
        self.assertEqual(parse(['-a', 'b', 'c', 'd']), {
            'a': 'b',
            '_': ['c', 'd']
        })

    def test_no_prefix(self):
        # cmd --no-input
        self.assertEqual(parse(['--no-input']), {'input': False, '_': []})

    def test_defaults(self):
        # cmd -a  # with b = 2 as default
        self.assertEqual(parse(['-a'], defaults={'b': 2}), 
                        {'a': True, 'b': 2 , '_': []})


class TestUtils(unittest.TestCase):

    def testInteger(self):
        self.assertTrue(isInteger('-1'))
        self.assertFalse(isInteger('ab'))

    def testFloat(self):
        self.assertTrue(isFloat('-1'))
        self.assertTrue(isFloat('-1.1'))
        self.assertFalse(isFloat('ab'))

    def testNumber(self):
        self.assertEqual(parseNumber('1.1'), 1.1)
        self.assertEqual(parseNumber('-1'), -1)


if __name__ == '__main__':
    unittest.main()
