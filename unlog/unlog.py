import sys
import re


class Unlog:
    """Unlog the output according to pattern passed in the *args* argument."""
    def __init__(self, args):
        self._args = args
        self._check_args()
        if args.start_pattern:
            self._filter_from_args()
    def _check_args(self):
        if not self._args.files and not self._args.start_pattern:
            sys.stderr.write('You must give a file or a start pattern.\n')
            sys.exit(2)

    def _filter_from_args(self):
        """Filter the files or stdin according to the patterns give by the
        arguments provided on the command line.
        """
        self._output_filter = Filter(error_pattern=self._args.error_pattern,
                                     start_pattern=self._args.start_pattern)
        # If no files are provided, read from stdin
        if self._args.files:
            self._files = self._args.files
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
