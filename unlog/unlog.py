import sys
import re
import os
import configparser


class Unlog:
    """Unlog the output according to pattern passed in the *args* argument."""
    def __init__(self, args):
        self._args = args
        self._check_args()
        if args.start_pattern:
            self._filter_from_args()
        else:
            self._filter_from_config()

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

    def _filter_from_config(self):
        """Filter the files according to the patterns defined in the config files."""
        self._load_config(self._args.config_file)
        for file in self._args.files:
            file = self._correct_path_input_file(file)
            self.process_file_filter_from_config(file)

    def _correct_path_input_file(self, file):
        """Expand the ~ variable and transform a relative path into an absolute one."""
        file = os.path.expanduser(file)
        file = os.path.abspath(file)
        return file

    def process_file_filter_from_config(self, file):
        """Process the file with the filters defined in config."""
        if self._file_in_config(self._config, file):
            self._output_filter = Filter(error_pattern=self._config[file]['error pattern'],
                                         start_pattern=self._config[file]['start pattern'])
            self.process_file(file)

    def _file_in_config(self, config, file):
        if file not in config:
            sys.stderr.write('{} is not in the config file {}'\
                             .format(file, self._args.config_file))
            return False
        return True

    def _load_config(self, config_file):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)


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
