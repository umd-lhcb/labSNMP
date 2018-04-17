#!/usr/bin/env python
#
# Last Change: Tue Apr 17, 2018 at 12:16 AM -0400

from pysnmp.hlapi import *

from labSNMP.wrapper.base import BiDict, BasePowerSupplyControl


class TrippLiteControl(BasePowerSupplyControl):
    community = 'tripplite'
    total_chs = 14
    power_status_code = BiDict({
        'idle':  '0',
        'off':   '1',
        'on':    '2',
        'cycle': '3'
    })

    MIB = 'TRIPPLITE-PRODUCTS'
    ch_ctrl = 'tlpPduOutletCommand'
    bulk_ctrl = 'tlpPduDeviceMainLoadCommand'
    ch_status = 'tlpPduOutletState'

    def PowerOffCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['off']
        )

        return self.DoCmd(setCmd, oid)

    def PowerOnCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['on']
        )

        return self.DoCmd(setCmd, oid)

    def PowerCycleCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['cycle']
        )

        return self.DoCmd(setCmd, oid)

    def PowerOffAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '0'
        ),
            self.power_status_code['off']
        )

        return self.DoCmd(setCmd, oid)

    def PowerOnAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '0'
        ),
            self.power_status_code['on']
        )

        return self.DoCmd(setCmd, oid)

    def PowerCycleAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '0'
        ),
            self.power_status_code['cycle']
        )

        return self.DoCmd(setCmd, oid)
