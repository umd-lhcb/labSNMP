#!/usr/bin/env python
#
# Last Change: Mon Apr 16, 2018 at 11:56 PM -0400

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
        oidPowerOff = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['off']
        )

        return self.DoCmd(setCmd, oidPowerOff)
