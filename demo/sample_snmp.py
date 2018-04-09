#!/usr/bin/env python

import sys
from pysnmp.hlapi import *

# The 'Test' parameter shows how to pass a argument to the command.
oidtype = ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0), 'Test')

# if we replace 'getCmd' with 'nextCmd', we will loop through all commands
# presented in the 'SNMPv2' mib file.
querycmd = getCmd(SnmpEngine(),
                  CommunityData('public'),
                  UdpTransportTarget((sys.argv[1], 161)),
                  ContextData(),
                  oidtype)

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
