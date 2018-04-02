#!/usr/bin/env python
#
# Last Change: Sat Mar 17, 2018 at 07:24 PM -0400

import sys
import os.path as path

from pysnmp.hlapi import *
from pysnmp.smi import builder

# Specify the complied mib source
mibBuilder = builder.MibBuilder()
mibSources = mibBuilder.getMibSources() + \
    (builder.DirMibSource(
        path.join(path.dirname(__file__), '..', 'labSNMP', 'cmd')),)
mibBuilder.setMibSources(*mibSources)

# Load mib
mibBuilder.loadModules('TRIPPLITE-PRODUCTS')

# Get the name of the SMTP command that will be executed
cmd = ObjectIdentity('TRIPPLITE-PRODUCTS', sys.argv[1], 0)

# Perform lookup
g = getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget((sys.argv[2], 161)),
           ObjectType(cmd))
next(g)

# Printout the result
print(str(cmd))
