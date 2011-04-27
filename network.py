import dbus


def intToIP (integer):
    parts = []

    # FIXME: not sure if DBus will handle endianness...
    for i in range(0, 4):
	parts.append(str(integer & 0xFF))
	integer = integer >> 8

    return '.'.join(parts)

def listReducer (a, b):
    return a + b


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
    _managerConnections = 'ActiveConnections'

    # FIXME: need to remove duplicates
    def getNameservers (self):
	devices = self._getActiveDevices()
	nameservers = map(self._getDeviceNameservers, devices)
	nameservers = reduce(listReducer, nameservers)
	return map(intToIP, nameservers)

    def getNetworks (self):
	devices = self._getActiveDevices()
	addresses = map(self._getDeviceAddresses, devices)
	addresses = reduce(listReducer, addresses)
	return map(lambda a: (intToIP(a[0]), int(a[1]), intToIP(a[2])),
		addresses)

    def _getActiveDevices (self):
	manager = self._getObject(self._manager)
	connections = self._getProperty(manager, self._managerInterface,
		self._managerConnections)
	connections = map(self._getObject, connections)
	devices = map(self._getConnectionDevices, connections)
	return reduce(listReducer, devices)

    def _getConnectionDevices (self, connection):
	devices = self._getProperty(connection, self._connectionInterface,
		self._connectionDevices)
	return map(self._getObject, devices)

    def _getDeviceAddresses (self, device):
	config = self._getDeviceConfig(device)
	return self._getProperty(config, self._configInterface,
		self._configAddresses)

    def _getDeviceConfig (self, device):
	config = self._getProperty(device, self._deviceInterface,
		self._deviceConfig)
	return self._getObject(config)

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
    # TODO: need to implement this
    pass
