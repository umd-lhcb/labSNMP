#!/usr/bin/env python
#
# Last Change: Fri Mar 06, 2020 at 10:48 PM +0800

from pysnmp.hlapi.asyncio import *

from labSNMP.wrapper.base import BiDict, BasePowerSupplyControlAsync


class TrippLiteControl(BasePowerSupplyControlAsync):
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

    async def PowerOffCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['off']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerOnCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['on']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerCycleCh(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_ctrl, '1', str(ch_num)
        ),
            self.power_status_code['cycle']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerOffAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '1'
        ),
            self.power_status_code['off']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerOnAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '1'
        ),
            self.power_status_code['on']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def PowerCycleAll(self):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.bulk_ctrl, '1'
        ),
            self.power_status_code['cycle']
        )

        status = await self.DoCmd(setCmd, oid)
        return status

    async def ChStatus(self, ch_num):
        oid = ObjectType(ObjectIdentity(
            self.MIB,
            self.ch_status, '1', str(ch_num)
        ))

        status = await self.DoCmd(getCmd, oid)
        return status

    async def ChsAllStatus(self):
        status = []
        for i in range(1, self.total_chs+1):
            ch_status = await self.ChStatus(i)
            status.append(ch_status)
        return status
