#!/usr/bin/env python

from pysnmp.hlapi import *


x = ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)
g = getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('demo.snmplabs.com', 161)),
           ContextData(),
           ObjectType(x))

next(g)
print(str(x))
