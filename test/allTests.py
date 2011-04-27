#!/usr/bin/env python

import os
import os.path
import re
import string
import sys
import unittest


# This is basically a substitute for the TestLoader.discover method in
# Python 2.7

def discover (suite = None, directory = '.'):
    if suite == None:
	suite = unittest.TestSuite()
    entries = os.listdir(directory)

    for entry in entries:
	path = fullPath(entry, directory)
	if os.path.isdir(path):
	    discover(suite, path)
	elif re.match('^[^.]*_test\.py$', entry):
	    module = pathToModule(path)
	    print 'Adding test', module, '...'
	    suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module))

    return suite

def fullPath (entry, directory = '.'):
    return os.path.normpath(directory + '/' + entry)

def pathToModule (path):
    base = os.path.dirname(sys.argv[0])
    if re.match(base, path):
	path = path[len(base):].strip('/')
    path = string.replace(path[:-3], '/', '.')
    return path

def rebase ():
    base = os.path.dirname(sys.argv[0])
    sys.path[0:1] = [base, base + '/..']


rebase()
print 'Searching for tests...'
tests = discover()

unittest.TextTestRunner().run(tests)
