#!/usr/bin/env python3
#
# Last Change: Fri Mar 06, 2020 at 10:41 PM +0800

from os import environ
from os.path import dirname, abspath, join
from pysnmp.hlapi import *
from pysnmp.smi import builder

py_mib_path = join(dirname(dirname(abspath(__file__))), 'compiled')


def convert_float(num):
    num = num & 0xFFFFFFFF
    sign = num >> 31
    num = num & 0x7FFFFFFF
    exponent = num >> 23
    exponent += -127
    fraction = 0

    for x in range(1, 23, 1):
        fraction += (num & (1 << (23-x)) > 0) * pow(2, -x)

    ret_val = ((1+fraction) * pow(2, exponent) * (1-2*sign))
    return ret_val


class BiDict(dict):
    # NOTE: Here we implicitly assumed that the forward mapping is injective.
    def __init__(self, *args, **kwargs):
        super(BiDict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse[value] = key


class BasePowerSupplyControl(object):
    community = 'public'
    total_chs = 0
    power_status_code = BiDict({
        'on':    '0',
        'off':   '1',
        'cycle': '2'
    })

    def __init__(self, ip):
        # FIXME: Use environmental variable to enable PySNMP to load compiled
        # MIBs.
        environ['PYSNMP_MIB_PKGS'] = py_mib_path

        self.ip = ip
        self.mibBuilder = builder.MibBuilder()

    def DoCmd(self, cmd, oidtype):
        queryCmd = cmd(
            SnmpEngine(),
            CommunityData(self.community),
            UdpTransportTarget((self.ip, 161)),
            ContextData(),
            oidtype
        )
        status = []

        try:
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in queryCmd:

                if errorIndication:
                    status.append(1)
                    status.append(errorIndication)
                    break

                elif errorStatus:
                    status.append(2)
                    status.append(errorStatus)
                    break

                else:
                    status.append(0)
                    for varBind in varBinds:
                        for x in varBind:
                            status.append(x.prettyPrint())

        except Exception as err:
            status.append(255)
            status.append(err)

        return status

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

    def ChsAllStatus(self):
        pass


class BasePowerSupplyControlAsync(BasePowerSupplyControl):
    async def DoCmd(self, cmd, oidtype):
        snmp_engine = SnmpEngine()
        queryCmd = await cmd(
            snmp_engine,
            CommunityData(self.community),
            UdpTransportTarget((self.ip, 161)),
            ContextData(),
            oidtype
        )
        status = []

        try:
            for (errorIndication,
                 errorStatus,
                 errorIndex,
                 varBinds) in queryCmd:

                if errorIndication:
                    status.append(1)
                    status.append(errorIndication)
                    break

                elif errorStatus:
                    status.append(2)
                    status.append(errorStatus)
                    break

                else:
                    status.append(0)
                    for varBind in varBinds:
                        for x in varBind:
                            status.append(x.prettyPrint())

        except Exception as err:
            status.append(255)
            status.append(err)

        finally:
            snmp_engine.transportDispatcher.closeDispatcher()

        return status

    async def PowerOffCh(self, ch_num):
        pass

    async def PowerOnCh(self, ch_num):
        pass

    async def PowerCycleCh(self, ch_num):
        pass

    async def PowerOffAll(self):
        pass

    async def PowerOnAll(self):
        pass

    async def PowerCycleAll(self):
        pass

    async def ChStatus(self, ch_num):
        pass

    async def ChsAllStatus(self):
        pass
