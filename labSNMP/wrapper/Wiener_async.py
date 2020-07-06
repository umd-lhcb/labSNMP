#!/usr/bin/env python3
#
# Last Change: Sun Jun 28, 2020 at 02:43 AM +0800

from pysnmp.hlapi.asyncio import *

from labSNMP.wrapper.base import BiDict, BasePowerSupplyControlAsync, \
    convert_float


class WienerControl(BasePowerSupplyControlAsync):
    community = 'admin'
    total_chs = 12
    power_status_code = BiDict({
        'off': '0',
        'on':  '1',
    })

    MIB = 'WIENER-CRATE-MIB'
    ch_ctrl = 'outputSwitch'
    ch_current = 'outputMeasurementCurrent'

    async def PowerOffCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, str(ch_num)
        ),
            self.power_status_code['off']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerOnCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, str(ch_num)
        ),
            self.power_status_code['on']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerCycleCh(self, ch_num):
        statusOff = await self.PowerOffCh(ch_num)
        statusOn = await self.PowerOnCh(ch_num)

        if statusOn[0] == 0 and statusOff[0] == 0:
            return [0, (statusOff, statusOn)]
        else:
            return [255, (statusOff, statusOn)]

    async def PowerOffAll(self):
        status = []
        status_details = []
        for i in range(1, self.total_chs+1):
            value = await self.PowerOffCh(i)
            status.append(value[0])
            status_details.append(value[1:])

        if sum(status) == 0:
            return [0, status_details]
        else:
            return [255, status_details]

    async def PowerOnAll(self):
        status = []
        status_details = []
        for i in range(1, self.total_chs+1):
            value = await self.PowerOnCh(i)
            status.append(value[0])
            status_details.append(value[1:])

        if sum(status) == 0:
            return [0, status_details]
        else:
            return [255, status_details]

    async def PowerCycleAll(self):
        status = []
        status_details = []
        for i in range(1, self.total_chs+1):
            value = await self.PowerCycleCh(i)
            status.append(value[0])
            status_details.append(value[1:])

        if sum(status) == 0:
            return [0, status_details]
        else:
            return [255, status_details]

    async def ChStatus(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, str(ch_num)
        ))

        status = await self.DoCmd(getCmd, oid)
        return status

    async def ChCurrent(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_current, str(ch_num)
        ))

        ret_val = await self.DoCmd(getCmd, oid)
        if(len(ret_val) == 3):
            ret_val[2] = convert_float(int(ret_val[2], 16))
        return ret_val

    async def ChsAllStatus(self):
        status = []
        for i in range(1, self.total_chs+1):
            ch_status = await self.ChStatus(i)
            status.append(ch_status)
        return status
