#!/usr/bin/env python
#
# Last Change: Mon Apr 02, 2018 at 03:53 PM -0400

import sys
import os.path as path

from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler

# Compile mib
mibBuilder = builder.MibBuilder()
mibViewController = view.MibViewController(mibBuilder)
compiler.addMibCompiler(mibBuilder, sources=[
    'file:///home/syp/misc/researches/umd-jawahery/labSNMP/MIB',
    'http://mibs.snmplabs.com/asn1/@mib@'])

# Load mib
mibBuilder.loadModules('TRIPPLITE-PRODUCTS', 'TRIPPLITE', 'SNMPv2-MIB')

# Get the name of the SMTP command that will be executed
cmd = ObjectIdentity('TRIPPLITE-PRODUCTS', 'tlpHardware', 0)

# Perform lookup
g = getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget((sys.argv[1], 161)),
           ObjectType(cmd))
next(g)

# Printout the result
print(str(cmd))
