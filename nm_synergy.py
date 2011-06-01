#!/usr/bin/env python

import network
import os
import subprocess

from dbus.mainloop.glib import DBusGMainLoop
import gobject


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


DBusGMainLoop(set_as_default = True)
if os.fork() == 0:
    network.NetworkManager().registerConnectHandler(reconnect)
    gobject.MainLoop().run()
else:
    reconnect()
