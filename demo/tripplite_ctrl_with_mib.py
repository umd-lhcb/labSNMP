#!/usr/bin/env python
#
# Last Change: Mon Apr 02, 2018 at 05:34 PM -0400

import sys
from os.path import dirname, abspath, join

from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler

# The absolute path of the mib files
mib_path = 'file://' + join(
    dirname(dirname(abspath(__file__))), 'MIB', 'Tripp_Lite')

# Compile mib
mibBuilder = builder.MibBuilder()
mibViewController = view.MibViewController(mibBuilder)
compiler.addMibCompiler(mibBuilder, sources=[
    mib_path,
    'http://mibs.snmplabs.com/asn1/@mib@'])

# Load mib
mibBuilder.loadModules('TRIPPLITE-PRODUCTS', 'TRIPPLITE')

# Get the name of the SMTP command that will be executed
cmd = ObjectIdentity('TRIPPLITE-PRODUCTS', sys.argv[2], 0)

# Perform lookup
g = getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget((sys.argv[2], 161)),
           ContextData(),
           ObjectType(cmd))
next(g)

# Printout the result
print(str(cmd))
