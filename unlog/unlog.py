import sys
import re


class Unlog:
    def __init__(self, args):
        self._output_filter = Filter()
        if args.files:
            self._files = args.files
            self.process_files()
        else:
            self.process_stdin()

    def process_files(self):
        for file in self._files:
            self.process_file(file)

    def process_file(self, file):
        try:
            with open(file, 'r') as f:
                for line in f:
                    self._output_filter.process_line(line)
        except IOError as e:
            sys.stderr.write(str(e))
            sys.stderr.write("\n")

    def process_stdin(self):
        for line in iter(sys.stdin.readline, ''):
            self._output_filter.process_line(line)


class Filter:
    def __init__(self, error_pattern="(error|warning)",
            start_pattern=r"/home/assos/drupal7/sites/assos.centrale-marseille.fr.\w"):
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
