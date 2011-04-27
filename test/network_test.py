import unittest

import network
import re


class NetworkManagerTest(unittest.TestCase):
    manager = None

    ipPattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    def setUp (self):
	self.manager = network.NetworkManager()

    def test_getNetworks (self):
	networks = self.manager.getNetworks()
	self.assertTrue(isinstance(networks, list),
		"Expected a list of networks.")

	for entry in networks:
	    self.assertTrue(isinstance(entry, tuple),
		    "Expected network entry to be a tuple.")
	    self.assertTrue(isinstance(entry[0], str),
		    "Expected IP address to be a string.")
	    self.assertTrue(re.match(self.ipPattern, entry[0]),
		    "Invalid IP address.")
	    self.assertTrue(isinstance(entry[1], int),
		    "Expected prefix to be an integer.")
	    self.assertTrue(entry[1] >= 0 and entry[1] <= 32,
		    "Invalid network prefix.")
	    self.assertTrue(isinstance(entry[2], str),
		    "Expected gateway address to be a string.")
	    self.assertTrue(re.match(self.ipPattern, entry[2]),
		    "Invalid gateway address.")

    def test_getNameservers (self):
	nameservers = self.manager.getNameservers()
	self.assertTrue(isinstance(nameservers, list),
		"Expected a list of nameservers.")

	for entry in nameservers:
	    self.assertTrue(isinstance(entry, str),
		    "Expected nameserver to be a string.")
	    self.assertTrue(re.match(self.ipPattern, entry),
		    "Invalid IP address.")

class NetworkMatcherTest(unittest.TestCase):
    pass
