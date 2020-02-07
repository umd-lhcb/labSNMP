#!/usr/bin/env python
#
# Last Change: Fri Feb 07, 2020 at 10:43 PM +0800

from pysnmp.hlapi import *

from labSNMP.wrapper.base import BiDict, BasePowerSupplyControl, convert_float


class WienerControl(BasePowerSupplyControl):
    community = 'admin'
    total_chs = 12
    power_status_code = BiDict({
        'off': '0',
        'on':  '1',
    })

    MIB = 'WIENER-CRATE-MIB'
    ch_ctrl = 'outputSwitch'
    ch_current= 'outputMeasurementCurrent'

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
        status_details = []
        for i in range(1, self.total_chs+1):
            value = self.PowerOffCh(i)
            status.append(value[0])
            status_details.append(value[1:])

        if sum(status) == 0:
            return [0, status_details]
        else:
            return [255, status_details]

    def PowerOnAll(self):
        status = []
        status_details = []
        for i in range(1, self.total_chs+1):
            value = self.PowerOnCh(i)
            status.append(value[0])
            status_details.append(value[1:])

        if sum(status) == 0:
            return [0, status_details]
        else:
            return [255, status_details]

    def PowerCycleAll(self):
        status = []
        status_details = []
        for i in range(1, self.total_chs+1):
            value = self.PowerCycleCh(i)
            status.append(value[0])
            status_details.append(value[1:])

        if sum(status) == 0:
            return [0, status_details]
        else:
            return [255, status_details]

    def ChStatus(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, str(ch_num)
        ))

        return self.DoCmd(getCmd, oid)

    def ChCurrent(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_current, str(ch_num)
        ))

        ret_val = self.DoCmd(getCmd, oid)
        if(len(ret_val) == 3):
            ret_val[2] = convert_float(int(ret_val[2], 16))
        return ret_val

    def ChsAllStatus(self):
        status = []
        for i in range(1, self.total_chs+1):
            status.append(self.ChStatus(i))
        return status
