#!/usr/bin/env python3
#
# Last Change: Tue Apr 17, 2018 at 03:15 PM -0400

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
            self.bulk_ctrl, '1'
        ),
            self.power_status_code['off']
        )

        return self.DoCmd(setCmd, oid)

    def PowerOnAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '1'
        ),
            self.power_status_code['on']
        )

        return self.DoCmd(setCmd, oid)

    def PowerCycleAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '1'
        ),
            self.power_status_code['cycle']
        )

        return self.DoCmd(setCmd, oid)

    def ChStatus(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_status, '1', str(ch_num)
        ))

        return self.DoCmd(getCmd, oid)

    def ChsAllStatus(self):
        status = []
        for i in range(1, self.total_chs+1):
            status.append(self.ChStatus(i))
        return status
