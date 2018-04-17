#!/usr/bin/env python
#
# Last Change: Mon Apr 16, 2018 at 09:20 PM -0400

from argparse import ArgumentParser

import sys
sys.path.insert(0, '..')

from labSNMP.wrapper.TrippLite import TrippLiteControl


def parse_input():
    parser = ArgumentParser(
        description='Control the power states of the PSUs in our lab.',
    )

    required = parser.add_argument_group('required arguments')

    required.add_argument(
        '-t', '--target-host',
        dest='host', nargs=1, required=True,
        help='''
        specify the target remote host.
        '''
    )

    required.add_argument(
        '-m', '--mode',
        dest='mode', action='store',
        choices=['tripplite', 'wiener'],
        default='tripplite',
        help='''choose which PSU to control.
        possible options: tripplite and wiener.
        '''
    )

    parser.add_argument(
        'action', metavar='ACTION',
        type=str, nargs='+',
        help='''specify a specific action.'''
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_input()

    if args.mode == 'tripplite':
        controller = TrippLiteControl(args.host[0])
