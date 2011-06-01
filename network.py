import ConfigParser
import dbus
import os
import socket


def ipToInt (ip):
    parts = ip.split('.')

    integer = 0
    for part in parts:
	integer = integer << 8
	integer += int(part)

    return socket.htonl(integer)

def intToIp (integer):
    integer = socket.ntohl(integer)
    parts = []

    for i in range(0,4):
	parts.append(str(integer & 0xFF))
	integer = integer >> 8
    parts.reverse()
    return '.'.join(parts)

def listReducer (a, b):
    return a + b

def networkAddress (ip, prefix):
    integer = ipToInt(ip)
    mask = socket.htonl(0xFFFFFFFF << (32 - prefix))
    return intToIp(integer & mask)

class NetworkManager:
    _service = 'org.freedesktop.NetworkManager'
    _manager = '/org/freedesktop/NetworkManager'

    _propertiesInterface = 'org.freedesktop.DBus.Properties'
    _configInterface = 'org.freedesktop.NetworkManager.IP4Config'
    _connectionInterface = 'org.freedesktop.NetworkManager.Connection.Active'
    _deviceInterface = 'org.freedesktop.NetworkManager.Device'
    _managerInterface = 'org.freedesktop.NetworkManager'

    _configAddresses = 'Addresses'
    _connectionDevices = 'Devices'
    _configNameservers = 'Nameservers'
    _deviceConfig = 'Ip4Config'
    _deviceName = 'Interface'
    _managerConnections = 'ActiveConnections'

    _deviceStateChanged = 'StateChanged'

    _NM_DEVICE_STATE_ACTIVATED = 8

    def getNetworks (self):
	devices = self._getActiveDevices()
        names = map(self._getDeviceName, devices)
	addresses = map(self._getDeviceAddresses, devices)
        tuples = map(lambda n, a: (n, a), names, addresses)
        tuples = map(lambda t: [(str(t[0]), intToIp(a[0]), int(a[1]),
            intToIp(a[2])) for a in t[1]], tuples)
        tuples = reduce(listReducer, tuples)
        return tuples

    def foo (self, *args):
        print 'here!'

    def registerConnectHandler (self, handler):
        dbus.SystemBus().add_signal_receiver(
        	lambda *state: self._managerStateChange(handler, *state),
        	self._deviceStateChanged, self._deviceInterface)

    def _managerStateChange (self, handler, *state):
        if state[0] == self._NM_DEVICE_STATE_ACTIVATED:
            handler()

    def _getActiveDevices (self):
	manager = self._getObject(self._manager)
	connections = self._getProperty(manager, self._managerInterface,
		self._managerConnections)
	connections = map(self._getObject, connections)
	devices = map(self._getConnectionDevices, connections)
        # FIXME: need to check for duplicates ???
	return reduce(listReducer, devices)

    def _getConnectionDevices (self, connection):
	devices = self._getProperty(connection, self._connectionInterface,
		self._connectionDevices)
	return map(self._getObject, devices)

    def _getDeviceAddresses (self, device):
	config = self._getDeviceConfig(device)
        if config == None: addresses = []
        else: addresses = self._getProperty(config, self._configInterface,
                self._configAddresses)
	return addresses

    def _getDeviceConfig (self, device):
	config = self._getProperty(device, self._deviceInterface,
		self._deviceConfig)
        if config == '/': config = None
        else: config = self._getObject(config)
	return config

    def _getDeviceName (self, device):
        return self._getProperty(device, self._deviceInterface,
                self._deviceName)

    def _getDeviceNameservers (self, device):
	config = self._getDeviceConfig(device)
	return self._getProperty(config, self._configInterface,
		self._configNameservers)

    def _getObject (self, path):
	return dbus.SystemBus().get_object(self._service, path)

    def _getProperty (self, obj, interface, prop):
	proxy = dbus.Interface(obj, self._propertiesInterface)
	return proxy.Get(interface, prop)

class NetworkMatcher:
    interface = 'interface'
    address = 'address'
    prefix = 'prefix'
    gateway = 'gateway'

    _config = None
    
    # TODO: add support for default config file
    def __init__ (self, config = os.environ['HOME'] + '/.nm_synergy.conf'):
	self._config = ConfigParser.ConfigParser()
	self._config.read(config)

    def match (self):
	hosts = self._config.sections()
	networks = NetworkManager().getNetworks()

	for host in hosts:
            interface = self._config.get(host, self.interface)
	    address = self._config.get(host, self.address)
	    prefix = self._config.getint(host, self.prefix)
	    gateway = self._config.get(host, self.gateway)

	    for network in networks:
		if self._isMatch(network,
			(interface, address, prefix, gateway)):
		    return host
	return None

    def _isMatch (self, one, two):
        interface1 = one[0]
        interface2 = two[0]
	gateway1 = one[3]
	gateway2 = two[3]
	networkAddress1 = networkAddress(one[1], one[2])
	networkAddress2 = networkAddress(two[1], two[2])
	return interface1 == interface2 and \
                networkAddress1 == networkAddress2 and gateway1 == gateway2
