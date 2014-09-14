import re
import sys
import smtplib
from email.mime.text import MIMEText

class Filter:
    """Allow the output to be filtered according to the pattern."""
    def __init__(self, error_pattern="(error|warning)", start_pattern=r".*",
                 no_mail=False, mail_to=None, mail_from='unlog@localhost',
                 mail_subject='Unlog report', start_group_pattern=None,
                 end_group_pattern=None):
        self._stack = []
        self._mail_lines = []
        self._error_pattern = re.compile(error_pattern, re.I)
        self._start_patern = re.compile(start_pattern, re.I)
        self._no_mail = no_mail
        self._mail_to = mail_to
        self._mail_from = mail_from
        self._mail_subject = mail_subject
        self._start_group_pattern = re.compile(start_group_pattern) \
                                    if start_group_pattern else None
        self._end_group_pattern = re.compile(end_group_pattern) \
                                    if end_group_pattern else None
        self._group_message = ''

    def process_file(self, file):
        for line in file:
            self.process_line(line)
        self.send_mail()

    def process_line(self, line):
        self.check_start(line)
        if not self._must_ignore_line(line):
            self._stack.append(line)
        self.check_end(line)

    def check_start(self, line):
        if self._has_group_patterns()\
        and self._start_group_pattern.match(line):
            m = self._start_group_pattern.match(line)
            self._group_message = ' - '.join(m.groups())
            start_group_message = 'GROUP: {}\n'.format(self._group_message)
            if self._must_display_sdout():
                sys.stdout.write(start_group_message)
            else:
                self._mail_lines.append(start_group_message)
        elif self._start_patern.search(line):
            self.print_stack()
            self._stack = []

    def print_stack(self):
        if self.match() and self._must_display_sdout():
            for line in self._stack:
                sys.stdout.write(line)
        elif self.match():
            self._mail_lines.extend(self._stack)

    def match(self):
        for line in self._stack:
            if self._error_pattern.search(line):
                return True

    def _must_display_sdout(self):
        return self._no_mail or self._mail_to is None

    def _must_send_email(self):
        return not self._must_display_sdout()

    def send_mail(self):
        """Send the msg using the localhost as SMTP server."""
        if self._must_send_email():
            msg = self._prepare_message()
            self._send_message(msg)

    def _prepare_message(self):
        """Prepare the _stack so it can be send by email.

        **Returns** - a MIMEText containing the message.
        """
        msg = MIMEText(''.join(self._mail_lines))
        msg['Subject'] = self._mail_subject
        msg['From'] = self._mail_from
        msg['To'] = self._mail_to

        return msg

    def _send_message(self, msg):
        try:
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()
        except ConnectionRefusedError as e:
            sys.stderr.write('Sending email failed with the following message:\n')
            sys.stderr.write(str(e))
            sys.stderr.write('\n')
            sys.stderr.write('DEBUG: Message content:\n\n{}'.format(str(msg)))

    def _must_ignore_line(self, line):
        """Returns True if the line must not be appended to the _stack."""
        if self._has_group_patterns()\
        and (self._start_group_pattern.search(line) or self._end_group_pattern.search(line)):
            return True
        else:
            return False

    def _has_group_patterns(self):
        """Returns True if we must perform the checks that depend on group patterns."""
        return self._start_group_pattern is not None\
            and self._end_group_pattern is not None

    def check_end(self, line):
        """Append END GROUP to _stack if line matches the end_group_pattern and
        displays it.
        """
        if self._has_group_patterns() and self._end_group_pattern.match(line):
            end_group_message = 'END GROUP: {}\n'.format(self._group_message)
            self.print_stack()
            self._stack = []
            if self._must_display_sdout():
                sys.stdout.write(end_group_message)
            else:
                self._mail_lines.append(end_group_message)
