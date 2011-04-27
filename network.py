import dbus


def intToIP (integer):
    parts = []

    for i in range(0, 4):
	parts.append(str(integer & 0xFF))
	integer = integer >> 8

    return '.'.join(parts)


class NetworkManager:
    _propertiesInterface = 'org.freedesktop.DBus.Properties'

    _service = 'org.freedesktop.NetworkManager'
    _manager = '/org/freedesktop/NetworkManager'

    _deviceInterface = 'org.freedesktop.NetworkManager.Device'
    _configInterface = 'org.freedesktop.NetworkManager.IP4Config'

    _deviceState = 'State'
    _deviceConfig = 'Ip4Config'
    _configAddresses = 'Addresses'

    NM_DEVICE_STATE_ACTIVATED = 8

    _bus = None

    def getNetworks (self):
	devices = self._getActiveDevices()
	addresses = map(self._getDeviceAddresses, devices)
	addresses = reduce(lambda a, b: a + b, addresses)
	mapper = lambda a: (intToIP(a[0]), int(a[1]), intToIP(a[2]))
	return map(mapper, addresses)

    def _deviceIsActive (self, device):
	return self._getProperty(device, self._deviceInterface,
		self._deviceState) == self.NM_DEVICE_STATE_ACTIVATED

    def _getActiveDevices (self):
	manager = self._getObject(self._manager)
	devices = map(self._getObject, manager.GetDevices())
	return filter(self._deviceIsActive, devices)

    def _getBus (self):
	if self._bus == None:
	    self._bus = dbus.SystemBus()
	return self._bus

    def _getDeviceAddresses (self, device):
	config = self._getProperty(device, self._deviceInterface,
		self._deviceConfig)
	config = self._getObject(config)
	return self._getProperty(config, self._configInterface,
		self._configAddresses)

    def _getObject (self, path):
	bus = self._getBus()
	return bus.get_object(self._service, path)

    def _getProperty (self, obj, interface, prop):
	proxy = dbus.Interface(obj, self._propertiesInterface)
	return proxy.Get(interface, prop)
