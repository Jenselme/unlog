import re
import sys
import smtplib
from email.mime.text import MIMEText
from builtins import len
from subprocess import Popen, PIPE

class Filter:
    """Defines how to filter.
    """
    #: This template will be filled by the date and the command.
    _start_group_template = 'GROUP: {}\n'
    #: This template will be filled by the date and the command. 
    _end_group_template = 'END GROUP: {}\n\n'

    def __init__(self, error_pattern="(error|warning)", start_pattern=r".*",
                 no_mail=False, mail_to=None, mail_from='unlog@localhost',
                 mail_subject='Unlog report', start_group_pattern=None,
                 end_group_pattern=None, mail_server='localhost'):
        """**PARAMETERS**

    * *error_pattern* - A regular expression that match the lines containing the
      errors. They will be displayed. Default: '(error|warning)'
    * *start_pattern* - A regular expression that match the 1st line. Default: '(.*)'
    * *no_mail* - Disable the sending of email. It has no effect if mail_to is
      None. Default: False.
    * *mail_to* - Email to address to which the output of the command must be sent.
      Default: None
    * *mail_from* - Which address the email must be send to. Default: 'unlog@localhost'
    * *mail_subject* - The subject of the report email. Default: 'Unlog report'
    * *start_group_pattern* - An optional regular expression matching the start
       of a log group (eg the ouput of one command). Default: None.
    * *end_group_pattern* - An optional regual expression matching the end of a
      log group. Default: None.
    * *mail_server* - The SMTP server to use. Can also be sendmail.
        """
        self._stack = []
        self._mail_lines = []
        self._error_pattern = re.compile(error_pattern, re.I)
        self._start_pattern = re.compile(start_pattern, re.I)
        self._no_mail = no_mail
        self._mail_to = mail_to
        self._mail_from = mail_from
        self._mail_subject = mail_subject
        self._start_group_pattern = re.compile(start_group_pattern) \
                                    if start_group_pattern else None
        self._end_group_pattern = re.compile(end_group_pattern) \
                                    if end_group_pattern else None
        self._group_message = ''
        self._mail_server = mail_server

    def process_file(self, file):
        """Loop over each line of a file and process them with
        :py:meth:`process_line`.
        """
        for line in file:
            self.process_line(line)
        # We must print the stack when we reach the end of a file so that the
        # errors located at the end are displayed.
        self.print_stack()
        self.send_mail()

    def process_line(self, line):
        """Calls :py:meth:`check_start` for each line and add the line to the
        stack unless it must be ignored. Finally call :py:meth:`check_end`.
        """
        self.check_start(line)
        if not self._must_ignore_line(line):
            self._stack.append(line)
        self.check_end(line)

    def check_start(self, line):
        """Checks if the current line match the start group or start pattern. Empty
        the stack if it matches a start pattern.
        """
        if self._has_group_patterns()\
        and self._start_group_pattern.match(line):
            m = self._start_group_pattern.match(line)
            self._group_message = ' - '.join(m.groups())
            start_group_message = self._start_group_template.format(self._group_message)
            if self._must_display_sdout():
                sys.stdout.write(start_group_message)
            else:
                self._mail_lines.append(start_group_message)
        elif self._start_pattern.search(line):
            self.print_stack()
            self._stack = []

    def print_stack(self):
        """Prints the stack to stdout or add the line the _email_lines list.
        """
        if self.match() and self._must_display_sdout():
            for line in self._stack:
                sys.stdout.write(line)
        elif self.match():
            self._mail_lines.extend(self._stack)

    def match(self):
        """Returns True if at least a line of the stack matche the error pattern.
        """
        for line in self._stack:
            if self._error_pattern.search(line):
                return True

    def _must_display_sdout(self):
        """Returns True must the output must be displayed on stdout.
        """
        return self._no_mail or self._mail_to is None

    def send_mail(self):
        """Send the msg using the localhost as SMTP server. If no SMTP server is
        available on localhost, it will crash.
        """
        if self._must_send_email():
            msg = self._prepare_message()
            self._send_message(msg)

    def _must_send_email(self):
        """Returns True if the output must be send by email.

        If there is no data to unlog, no email is send.
        """
        self._filter_mail_lines()
        return not self._must_display_sdout() and self._mail_lines

    def _filter_mail_lines(self):
        """Remove the start and end group lines if the group is empty."""
        # Remove the dict from the templates to use startwith.
        start_group = self._start_group_template[:-3]
        end_group = self._end_group_template[:-4]
        for index in range(len(self._mail_lines) - 1):
            if self._mail_lines[index].startswith(start_group) and\
            self._mail_lines[index + 1].startswith(end_group):
                self._mail_lines[index] = ''
                self._mail_lines[index + 1] = ''
        self._remove_empty_string_in_mail_lines()

    def _remove_empty_string_in_mail_lines(self):
        self._mail_lines = [line for line in self._mail_lines if line]

    def _prepare_message(self):
        """Prepare the _stack so it can be send by email.

        **RETURN** - a MIMEText containing the message.
        """
        msg = MIMEText(''.join(self._mail_lines))
        msg['Subject'] = self._mail_subject
        msg['From'] = self._mail_from
        msg['To'] = self._mail_to

        return msg

    def _send_message(self, msg):
        """Send a MIMEText message or print an error to stderr in case of failure.
        """
        try:
            if self._mail_server.endswith('/sendmail'):
                # Use sendmail instead of an SMTP server
                p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
                p.communicate(msg.as_string())
            else:
                s = smtplib.SMTP(self._mail_server)
                err = s.send_message(msg)
                if err:
                    print(err)
                s.quit()
        except Exception as e:
            sys.stderr.write('Sending email failed with the following message:\n')
            sys.stderr.write(str(e))
            sys.stderr.write('\n')
            sys.stderr.write('DEBUG: Message content:\n\n{}'.format(str(msg)))

    def _must_ignore_line(self, line):
        """Returns True if the line must not be appended to the _stack.
        """
        if self._has_group_patterns()\
        and (self._start_group_pattern.search(line) or self._end_group_pattern.search(line)):
            return True
        else:
            return False

    def _has_group_patterns(self):
        """Returns True if we must perform the checks that depend on group patterns.
        """
        return self._start_group_pattern is not None\
            and self._end_group_pattern is not None

    def check_end(self, line):
        """Append END GROUP to _stack if line matches the end_group_pattern and
        displays it.
        """
        if self._has_group_patterns() and self._end_group_pattern.match(line):
            end_group_message = self._end_group_template.format(self._group_message)
            self.print_stack()
            self._stack = []
            if self._must_display_sdout():
                sys.stdout.write(end_group_message)
            else:
                self._mail_lines.append(end_group_message)
