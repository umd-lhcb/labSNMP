#!/usr/bin/env python
#
# Last Change: Mon Apr 02, 2018 at 05:18 PM -0400

import sys
import os.path as path

from pysnmp.hlapi import *
from pysnmp.smi import builder

# Specify the complied mib source
mibBuilder = builder.MibBuilder()
mibSources = mibBuilder.getMibSources() + \
    (builder.DirMibSource(
        path.join(path.dirname(__file__), '..', 'MIB', 'Tripp_Lite')),)
mibBuilder.setMibSources(*mibSources)

# Load mib
mibBuilder.loadModules('TRIPPLITE-PRODUCTS')

# Get the name of the SMTP command that will be executed
# cmd = ObjectIdentity('TRIPPLITE-PRODUCTS', sys.argv[1], 0)

# # Perform lookup
# g = getCmd(SnmpEngine(),
           # CommunityData('tripplite'),
           # UdpTransportTarget((sys.argv[2], 161)),
           # ContextData(),
           # ObjectType(cmd))

# print(next(g))

# # Printout the result
# print(str(cmd))
