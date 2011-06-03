import os
import os.path
import signal
import sys

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject


_PIDFile = os.environ['HOME'] + '/.nm_synergy.pid'


def createPIDFile (path = _PIDFile):
    with open(path, 'w') as file:
        file.write(str(os.getpid()))

def deletePIDFile (path = _PIDFile):
    os.remove(path)

def exitHandler (*args):
    deletePIDFile()
    sys.exit()

def init (path = _PIDFile):
    # FIXME: need to investigate atomic file creation in Python...
    if os.path.isfile(path): sys.exit()
    else: createPIDFile()
    DBusGMainLoop(set_as_default = True)

# NOTE: signal handlers need to be registered prior to main loop forking/running.
def fork ():
    if os.fork() == 0:
        signal.signal(signal.SIGTERM, exitHandler)
        signal.signal(signal.SIGINT, exitHandler)
        gobject.MainLoop().run()
