#!/usr/bin/env python
#
# Last Change: Thu Apr 12, 2018 at 05:23 PM -0400

from os import environ
from os.path import dirname, abspath, join
from pysnmp.hlapi import *
from pysnmp.smi import builder

py_mib_path = join(dirname(dirname(abspath(__file__))), 'compiled')


class BasePowerSupplyControl(object):
    community = 'public'
    total_chs = 0
    power_status_code = {
        'on': 0,
        'off': 1,
        'cycle': 2
    }

    def __init__(self, ip):
        # FIXME: Use environmental variable to enable PySNMP to load compiled
        # MIBs.
        environ['PYSNMP_MIB_PKGS'] = py_mib_path

        self.ip = ip
        self.mibBuilder = builder.MibBuilder()

    def DoCmd(self, cmd, oidtype):
        cmd(
            SnmpEngine(),
            CommunityData(self.community),
            UdpTransportTarget((self.ip, 161)),
            ContextData(),
            oidtype
        )

    def PowerOffCh(self, ch_num):
        pass

    def PowerOnCh(self, ch_num):
        pass

    def PowerCycleCh(self, ch_num):
        pass

    def PowerOffAll(self):
        pass

    def PowerOnAll(self):
        pass

    def PowerCycleAll(self):
        pass

    def ChStatus(self, ch_num):
        pass
