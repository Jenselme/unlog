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
    parser.add_argument('--mail-to', '-t', dest='mail_to',
                        help='Send the report by email to the provided address '
                        'instead of printing the result to the command line. If'
                        ' a mail address is present in the configuration file, '
                        'this parameter will override it.')
    parser.add_argument('--mail-from', '-f', dest='mail_from',
                        help='Send the email with this address in the FROM field.'
                        ' If a from address is present in the configuration file,'
                        ' this parameter override it.')
    parser.add_argument('--mail-subject', dest='mail_subject',
                        help='The subject of the email to send.')
    parser.add_argument('--no-mail', dest='no_mail', action='store_true',
                        help='Print the output to stdout, even if a mail address'
                        ' is provided.')
    args = parser.parse_args()

    Unlog(args)


if __name__ == '__main__':
    main()
