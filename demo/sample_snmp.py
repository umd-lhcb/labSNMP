#!/usr/bin/env python

import sys
from pysnmp.hlapi import *

x = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
g = getCmd(SnmpEngine(),
           CommunityData('tripplite'),
           UdpTransportTarget((sys.argv[1], 161)),
           ContextData(),
           ObjectType(x))

result = next(g)
print(result)
print(str(x))
