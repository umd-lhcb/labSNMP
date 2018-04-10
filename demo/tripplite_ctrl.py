#!/usr/bin/env python
#
# Last Change: Mon Apr 09, 2018 at 06:05 PM -0400

import sys
from os.path import dirname, abspath, join

from pysnmp.hlapi import *
from pysnmp.smi import builder, compiler

# The absolute path of the mib files
mib_path = 'file://' + join(
    dirname(dirname(abspath(__file__))), 'labSNMP', 'MIB', 'Tripp_Lite')

# Compile mib
mibBuilder = builder.MibBuilder()
compiler.addMibCompiler(mibBuilder, sources=[
    mib_path,
    'http://mibs.snmplabs.com/asn1/@mib@'])

# Load mib
mibBuilder.loadModules('TRIPPLITE-PRODUCTS')

oidtype = ObjectType(ObjectIdentity('TRIPPLITE-PRODUCTS',
                                    'tlpCooling'))
# On the trailing numbers:
#   A scalar type OID has only one entry, and should always followed by a '0.
#

# tlpAtsOutputCurrent
# tlpAtsInputPhaseCurrent
# tlpDeviceTable
# tlpDeviceNumDevices
# tlpEnvIdentEntry
# tlpPduHeatsinkIndex
# tlpPduHeatsinkTable
# tlpPduHeatsinkEntry
# tlpPduHeatsinkTemperatureF
# tlpPduHeatsinkTemperatureC
# tlpPduControlPduOff

someCmd = nextCmd if len(sys.argv) > 2 and sys.argv[2] == 'loop' else getCmd
querycmd = someCmd(SnmpEngine(),
                  CommunityData('tripplite'),
                  UdpTransportTarget((sys.argv[1], 161)),
                  ContextData(),
                  oidtype)

# Perform lookup, traverse the whole mib file
for (errorIndication,
     errorStatus,
     errorIndex,
     varBinds) in querycmd:

    if errorIndication:
        print(errorIndication)
        break

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                      errorIndex and varBinds[int(errorIndex) - 1][0] or
                      '?'))
        break

    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))
