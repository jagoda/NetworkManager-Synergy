Introduction
============

`nm_synergy` is a simple DBus client written in Python that will automatically
connect to Synergy servers based on the current network environment. The client
spawns an event loop process to listen for state changes in order to
adapt to changing network conditions.

Currently `nm_synergy` requires that Synergy (server and client) be configured
completely separately.

Client Configuration
====================

Client configuration is stored in an INI file called `.nm_synergy.conf` in the
user's home directory. The file looks something like the following:

    [192.168.2.1]
    interface=eth0
    prefix=24
    address=192.168.2.29
    gateway=192.168.2.254

The section headings define the target Synergy server to match. The
client will use the address and prefix to compute a network address. A match
occurs if and only if the named interface on the system has a matching network
address and gateway.

(Optional) System Configuration
===============================

While `nm_synergy` works fine when launched manually (independent of system
setup), it's value is largely increased by having the daemon be launched
automatically by the client system. Exactly how this configuration is
performed depends on the specific system being configured.

GDM
---

The GDM login manager has configuration hooks that allow spawning processes
pre-login. All of these processes are run as the `gdm` user. When GDM is
configured to launch `nm_synergy` pre-login, peripheral sharing can occur
starting from the login screen.

*FIXME:* document (or link to) GDM configuration steps.

User Sessions
-------------

`nm_synergy` can also be configured to run within a specified user session. This
has the same effect as launching the daemon from GDM with the exception that
the actual login step will need to leverage the local keyboard and mouse.

*FIXME:* document (or link to) session specific configuration.
