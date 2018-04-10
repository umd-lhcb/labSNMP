#!/usr/bin/env python
#
# Last Change: Mon Apr 09, 2018 at 11:20 PM -0400

from argparse import HelpFormatter, ArgumentParser


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


if __name__ == "__main__":
    args = parse_input()
