import errno
import os
import os.path
import signal
import sys

import dbus
from dbus.mainloop.glib import DBusGMainLoop
import gobject


_PIDFile = os.environ['HOME'] + '/.nm_synergy.pid'


def checkPID (path):
    if os.path.isfile(path):
        pid = 0
        with open(path, 'r') as file:
            pid = int(file.read())

        alive = True
        try:
            os.kill(pid, signal.SIGCONT)
        except OSError as (error, stderr):
            if error == errno.ESRCH:
                alive = False

        if alive: sys.exit()
        else: os.remove(path)

def createPIDFile (path, pid):
    with open(path, 'w') as file:
        file.write(str(pid))

def deletePIDFile (path = _PIDFile):
    os.remove(path)

def exitHandler (*args):
    deletePIDFile()
    sys.exit()

# NOTE: signal handlers need to be registered prior to main loop forking/running.
# NOTE: signal handlers only work for "clean" exit. checkPID is used to clean up
#   after a "dirty" exit.
def fork (path = _PIDFile):
    pid = os.fork()
    if pid == 0:
        signal.signal(signal.SIGTERM, exitHandler)
        signal.signal(signal.SIGINT, exitHandler)
        gobject.MainLoop().run()
    else:
        createPIDFile(path, pid)

def init (path = _PIDFile):
    # FIXME: need to investigate atomic file creation in Python...
    checkPID(path)
    DBusGMainLoop(set_as_default = True)
