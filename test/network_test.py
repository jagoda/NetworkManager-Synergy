import unittest

import ConfigParser
import os
import re
import socket

import network


class NetworkUtilsTest(unittest.TestCase):
    def test_ipToInt (self):
	self.assertEqual(0xFFFFFFFF, network.ipToInt('255.255.255.255'))
	self.assertEqual(socket.htonl(0x01020304), network.ipToInt('1.2.3.4'))

    def test_intToIp (self):
	self.assertEqual('255.255.255.255', network.intToIp(0xFFFFFFFF))
	self.assertEqual('1.2.3.4', network.intToIp(socket.htonl(0x01020304)))

    def test_listReducer (self):
	self.assertEqual([1, 2, 3], network.listReducer([1], [2, 3]))

    def test_networkAddress (self):
	self.assertEqual('1.2.3.0', network.networkAddress('1.2.3.4', 24))
	self.assertEqual('1.2.3.128', network.networkAddress('1.2.3.254', 25))

class NetworkManagerTest(unittest.TestCase):
    manager = network.NetworkManager()

    ipPattern = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    def test_getNetworks (self):
	networks = self.manager.getNetworks()
	self.assertTrue(isinstance(networks, list),
		"Expected a list of networks.")

	for entry in networks:
	    self.assertTrue(isinstance(entry, tuple),
		    "Expected network entry to be a tuple.")
            self.assertTrue(isinstance(entry[0], str),
                    "Expected interface to be a string.")
	    self.assertTrue(isinstance(entry[1], str),
		    "Expected IP address to be a string.")
	    self.assertTrue(re.match(self.ipPattern, entry[1]),
		    "Invalid IP address.")
	    self.assertTrue(isinstance(entry[2], int),
		    "Expected prefix to be an integer.")
	    self.assertTrue(entry[2] >= 0 and entry[2] <= 32,
		    "Invalid network prefix.")
	    self.assertTrue(isinstance(entry[3], str),
		    "Expected gateway address to be a string.")
	    self.assertTrue(re.match(self.ipPattern, entry[3]),
		    "Invalid gateway address.")

class NetworkMatcherTest(unittest.TestCase):
    config = 'test.conf'
    matcher = None

    def setUp (self):
	self._createConfig()
	self.matcher = network.NetworkMatcher(self.config)

    def tearDown (self):
        os.remove(self.config)

    def test_match (self):
	self.assertEqual('foo.bar.somewhere.com', self.matcher.match())

    def _createConfig (self):
	manager = network.NetworkManager()
	networks = manager.getNetworks()
	host = 'foo.bar.somewhere.com'
	
	config = ConfigParser.ConfigParser()
	config.add_section(host)
        config.set(host, network.NetworkMatcher.interface, networks[0][0])
	config.set(host, network.NetworkMatcher.address, networks[0][1])
	config.set(host, network.NetworkMatcher.prefix, networks[0][2])
	config.set(host, network.NetworkMatcher.gateway, networks[0][3])
	with open(self.config, 'w') as configFile:
	    config.write(configFile)
