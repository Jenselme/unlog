#!/usr/bin/python3

import argparse
try:
    from unlog import Unlog
except ImportError:
    from unlog.unlog import Unlog


def main():
    parser = argparse.ArgumentParser(description='Filter print the line of the outpu from a starting pattern to an end pattern.')
    parser.add_argument('files', metavar='files', nargs='*',
                        help='The file which must be unlogged.')
    args = parser.parse_args()

    Unlog(args)


if __name__ == '__main__':
    main()
