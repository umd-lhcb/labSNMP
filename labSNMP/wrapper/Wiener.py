#!/usr/bin/env python
#
# Last Change: Tue Apr 17, 2018 at 12:53 AM -0400

from pysnmp.hlapi import *

from labSNMP.wrapper.base import BiDict, BasePowerSupplyControl


class WienerControl(BasePowerSupplyControl):
    community = 'admin'
    total_chs = 14
    power_status_code = BiDict({
        'off': '0',
        'on':  '1',
        'setVoltageMeasurementOn': '21',
        'setRippleMeasurementOn':  '22'
    })

    MIB = 'WIENER-CRATE-MIB'
    ch_ctrl = 'outputSwitch'
    ch_voltage = 'outputVoltage'
    ch_current = 'outputCurrent'

    def PowerOffCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, str(ch_num)
        ),
            self.power_status_code['off']
        )

        return self.DoCmd(setCmd, oid)

    def PowerOnCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, str(ch_num)
        ),
            self.power_status_code['on']
        )

        return self.DoCmd(setCmd, oid)

    def PowerCycleCh(self, ch_num):
        statusOff = self.PowerOffCh(ch_num)
        statusOn = self.PowerOnCh(ch_num)

        if statusOn[0] == 0 and statusOff[0] == 0:
            return [0, (statusOff, statusOn)]
        else:
            return [255, (statusOff, statusOn)]

    def PowerOffAll(self):
        status = []
        for i in range(1, self.total_chs+1):
            status.append(self.PowerOffCh(i)[0])

        if sum(status) == 0:
            return [0, ]
        else:
            return [255, ]

    def PowerOnAll(self):
        status = []
        for i in range(1, self.total_chs+1):
            status.append(self.PowerOnCh(i)[0])

        if sum(status) == 0:
            return [0, ]
        else:
            return [255, ]

    def PowerCycleAll(self):
        statusOff = self.PowerOffAll()
        statusOn = self.PowerOnAll()

        if statusOn[0] == 0 and statusOff[0] == 0:
            return [0, ]
        else:
            return [255, ]

    def ChStatus(self, ch_num):
        pass
        # oid = ObjectType(ObjectIdentity(
            # self.MIB,
            # self.ch_status, '1', str(ch_num)
        # ))

        # return self.DoCmd(getCmd, oid)

    def ChsAllStatus(self):
        status = []
        for i in range(1, self.total_chs+1):
            status.append(self.ChStatus(i))
        return status
