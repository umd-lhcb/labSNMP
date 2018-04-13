#!/usr/bin/env python
#
# Last Change: Fri Apr 13, 2018 at 12:14 PM -0400

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
    ch_ctrl = 'tlpPduOutletComand'
    bulk_ctrl = 'tlpPduDeviceMainLoadCommand'
    ch_status = 'tlpPduOutletState'

    def PowerOffCh(self, ch_num):
        oidPowerOff = OjectType(ObjectIdentity(self.MIB, self.ch_ctrl),
                                self.power_status_code['off']
                                )
        status = self.DoCmd(setCmd, oidPowerOff)

        print(status)
