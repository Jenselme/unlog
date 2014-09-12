import re
import sys

class Filter:
    """Allow the output to be filtered according to the pattern."""
    def __init__(self, error_pattern="(error|warning)",
            start_pattern=r".*"):
        self._stack = []
        self._error_pattern = re.compile(error_pattern, re.I)
        self._start_patern = re.compile(start_pattern, re.I)

    def process_line(self, line):
        self.check_start(line)
        self._stack.append(line)

    def check_start(self, line):
        if self._start_patern.search(line):
            self.print_stack()
            self._stack = []

    def print_stack(self):
        if self.match():
            for line in self._stack:
                sys.stdout.write(line)

    def match(self):
        for line in self._stack:
            if self._error_pattern.search(line):
                return True
