#!/usr/bin/env python

import network
import subprocess
import utils


def connect ():
    matcher = network.NetworkMatcher()
    host = matcher.match()
    
    if host != None:
	print "Spawning client for host '{0}'...".format(host)
	subprocess.call(['synergyc', host])

def disconnect ():
    subprocess.call(['killall', 'synergyc'])

def reconnect ():
    disconnect()
    connect()


utils.init()
network.NetworkManager().registerConnectHandler(reconnect)
reconnect()
