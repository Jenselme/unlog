#!/usr/bin/python3

import argparse
try:
    from unlog import Unlog
except ImportError:
    from unlog.unlog import Unlog


def main():
    parser = argparse.ArgumentParser(description='Filter print the line of the '
                                     'output from a starting pattern only if it '
                                     'contains an error pattern.')
    parser.add_argument('files', metavar='files', nargs='*',
                        help='The file which must be unlogged.')
    parser.add_argument('--start-pattern', '-s', dest='start_pattern',
                        help='The start pattern. Required to know where a group '
                        'of lines start.')
    parser.add_argument('--error-pattern', '-e', dest='error_pattern',
                        default=r'(error|warning)',
                        help='The error pattern. Only group of lines containing '
                        'this pattern will be printed')
    parser.add_argument('--config', '-c', dest='config_file', default='~/.unlog',
                        help='Use a different config file from ~/.unlog')
    args = parser.parse_args()

    Unlog(args)


if __name__ == '__main__':
    main()
