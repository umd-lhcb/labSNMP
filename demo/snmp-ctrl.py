#!/usr/bin/env python
#
# Last Change: Tue Apr 10, 2018 at 12:23 AM -0400

from os.path import dirname, abspath, join
from argparse import HelpFormatter, ArgumentParser
from pysnmp.hlapi import *
from pysnmp.smi import builder, compiler


class SmartFormatter(HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return HelpFormatter._split_lines(self, text, width)


def parse_input():
    parser = ArgumentParser(
        description='Perform SNMP lookup, walk through, and value set.',
        formatter_class=SmartFormatter
    )

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '-t', '--target-host',
        dest='host', nargs=1, required=True,
        help='''
        specify the target remote host.
        '''
    )

    parser.add_argument(
        'oids', metavar='OIDS',
        type=str, nargs='+',
        help='''
        specify a list of OIDs.'''
    )

    parser.add_argument(
        '-m', '--mode',
        dest='mode', action='store',
        choices=['walkthrough', 'lookup', 'set'],
        default='walkthrough',
        help='''R|choose operation mode. there are 3 available modes:
    walkthrough (default): perform SNMP lookup. In
        this mode, OIDs don't need to be precise.

    lookup: lookup a specified OID value on the agent.
        The OIDs need to be precise, and manual
        termination is needed.

    set: set a specified OID value. Need precise OIDs.'''
    )

    parser.add_argument(
        '-c', '--community',
        dest='community', nargs='?',
        default='tripplite',
        help='''
        specify the community for the SNMP action. by default 'tripplite' is
        used, which is suitable for talking to one of our lab PSU. for general
        purpose action, the 'public' community should be used.
        '''
    )

    return parser.parse_args()


def findCmd(mode):
    cmd_dict = {'walkthrough': nextCmd,
                'lookup': getCmd,
                'set': setCmd}
    return cmd_dict[mode]


def isInt(s):
    try:
        return int(s)

    except ValueError:
        return s


if __name__ == "__main__":
    args = parse_input()

    # Specify the absolute path of the MIB files
    tripplite_mib_path = 'file://' + join(
        dirname(dirname(abspath(__file__))), 'labSNMP', 'MIB', 'Tripp_Lite')

    # Compile MIB
    mibBuilder = builder.MibBuilder()
    compiler.addMibCompiler(mibBuilder, sources=[
        tripplite_mib_path,
        'http://mibs.snmplabs.com/asn1/@mib@'])

    # Load MIB
    mibBuilder.loadModules('TRIPPLITE-PRODUCTS')

    oidtype = ObjectType(ObjectIdentity(*args.oids))
    queryCmd = findCmd(args.mode)(
        SnmpEngine(),
        CommunityData(args.community),
        UdpTransportTarget((args.host[0], 161)),
        ContextData(),
        oidtype)

    try:
        for (errorIndication,
             errorStatus,
             errorIndex,
             varBinds) in queryCmd:

            if errorIndication:
                print(errorIndication)
                break

            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or
                            '?'))
                break

            else:
                for varBind in varBinds:
                    print(' = '.join([x.prettyPrint() for x in varBind]))

    except KeyboardInterrupt:
        pass

    except Exception as err:
        print(err)
