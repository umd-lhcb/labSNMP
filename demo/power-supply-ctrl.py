#!/usr/bin/env python
#
# Last Change: Tue Apr 17, 2018 at 12:27 AM -0400

from argparse import ArgumentParser

import sys
sys.path.insert(0, '..')

from labSNMP.wrapper.TrippLite import TrippLiteControl


def parse_input():
    parser = ArgumentParser(
        description='Control the power states of the PDUs in our lab.',
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


class InputToPduAction(object):
    def __init__(self, controller, input):
        self.controller = controller
        self.input = input

    def do(self):
        try:
            assert self.check_input_validity()
            if len(self.input) == 3:
                if self.input[2] == 'off':
                    print(self.controller.PowerOffCh(self.input[1]))
                if self.input[2] == 'on':
                    print(self.controller.PowerOnCh(self.input[1]))
                if self.input[2] == 'cycle':
                    print(self.controller.PowerCycleCh(self.input[1]))
                if self.input[2] == 'status':
                    print(self.controller.ChStatus(self.input[1]))
            else:
                if self.input[0] == 'off':
                    print(self.controller.PowerOffAll())
                if self.input[0] == 'on':
                    print(self.controller.PowerOnAll())
                if self.input[2] == 'cycle':
                    print(self.controller.PowerCycleAll())
                if self.input[2] == 'status':
                    print(self.controller.ChsAllStatus())

        except AssertionError:
            print('Invalid input: %s' % self.input)
        except Exception as err:
            print(err)

    def check_input_validity(self):
        if len(self.input) == 1 or len(self.input) == 3:
            boolean_list = map(self.valid_keywords, self.input)
            if True in boolean_list:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def valid_keywords(word):
        if word in ('off', 'on', 'cycle', 'status'):
            return True
        else:
            return False


if __name__ == "__main__":
    args = parse_input()

    if args.mode == 'tripplite':
        controller = TrippLiteControl(args.host[0])
        worker = InputToPduAction(controller, args.action)
        worker.do()
    elif args.mode == 'wiener':
        pass
        # controller = TrippLiteControl(args.host[0])
        # worker = InputToPduAction(controller, args.action)
        # worker.do()
