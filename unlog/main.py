#!/usr/bin/python3

"""
usage: main.py [-h] [--start-pattern START_PATTERN]
               [--error-pattern ERROR_PATTERN] [--config CONFIG_FILE]
               [--use-config-section USE_CONFIG_SECTION] [--mail-to MAIL_TO]
               [--mail-from MAIL_FROM] [--mail-subject MAIL_SUBJECT]
               [--mail-server SMTP_SERVER]
               [--no-mail] [--start-group START_GROUP_PATTERN]
               [--end-group END_GROUP_PATTERN]
               [--encoding ENCODING]
               [files [files ...]]

Filter print the line of the output from a starting pattern only if it
contains an error pattern.

positional arguments:
  files                 The file which must be unlogged.

optional arguments:
  -h, --help            show this help message and exit
  --start-pattern START_PATTERN, -s START_PATTERN
                        The start pattern. Required to know where a group of
                        lines start.
  --error-pattern ERROR_PATTERN, -e ERROR_PATTERN
                        The error pattern. Only group of lines containing this
                        pattern will be printed
  --config CONFIG_FILE, -c CONFIG_FILE
                        Use a different config file from ~/.unlog
  --use-config-section USE_CONFIG_SECTION, -u USE_CONFIG_SECTION
                        Unlog will use the provided config section to process
                        the file or stdin.
  --mail-to MAIL_TO, -t MAIL_TO
                        Send the report by email to the provided address
                        instead of printing the result to the command line. If
                        a mail address is present in the configuration file,
                        this parameter will override it.
  --mail-from MAIL_FROM, -f MAIL_FROM
                        Send the email with this address in the FROM field. If
                        a from address is present in the configuration file,
                        this parameter override it.
  --mail-subject MAIL_SUBJECT
                        The subject of the email to send.
  --mail-server
                        The SMTP server to use. Can also be sendmail. Default is
                        localhost.
  --no-mail             Print the output to stdout, even if a mail address is
                        provided.
  --start-group START_GROUP_PATTERN
                        Pattern to start a group.
  --end-group END_GROUP_PATTERN
                        Pattern to end a group. A line that match this pattern
                        will be ignored.
  --encoding ENCODING
                        The encoding of the file to unlog. By default it is UTF-8.
"""

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
    parser.add_argument('--use-config-section', '-u', dest='use_config_section',
                        help='Unlog will use the provided config section to '
                        'process the file or stdin.')
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

    parser.add_argument('--mail-server', dest='mail_server', default='localhost',
                        help='The SMTP server to use. Can also be sendmail.'
                        ' Default is localhost.')
    parser.add_argument('--no-mail', dest='no_mail', action='store_true',
                        help='Print the output to stdout, even if a mail address'
                        ' is provided.')
    parser.add_argument('--start-group', dest='start_group_pattern',
                        help='Pattern to start a group.')
    parser.add_argument('--end-group', dest='end_group_pattern',
                        help='Pattern to end a group. A line that match this '
                        'pattern will be ignored.')
    parser.add_argument('--encoding', dest='log_encoding', default='utf-8',
                        help='The encoding of the file to unlog')
    args = parser.parse_args()

    Unlog(args)


if __name__ == '__main__':
    main()
