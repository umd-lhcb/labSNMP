#!/usr/bin/env python
#
# Last Change: Thu Mar 15, 2018 at 02:32 PM -0400

from pysnmp.hlapi import *
from pysnmp.smi import builder

# Specify

g = getCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('demo.snmplabs.com', 161)))
