import sys
import os
import copy

try:
    from config import Config
    from filter import Filter
except ImportError:
    from unlog.config import Config
    from unlog.filter import Filter


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
        config = copy.copy(self._args.__dict__)
        del config['files']
        del config['config_file']
        self._output_filter = Filter(**config)
        # If no files are provided, read from stdin
        if self._args.files:
            self._files = self._args.files
            self.process_files()
        else:
            self.process_stdin()

    def process_files(self):
        for file in self._files:
            self.process_file(file)

    def process_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self._output_filter.process_file(file)
        except IOError as e:
            sys.stderr.write(str(e))
            sys.stderr.write("\n")

    def process_stdin(self):
        for line in iter(sys.stdin.readline, ''):
            self._output_filter.process_line(line)
        self._output_filter.send_mail()

    def _filter_from_config(self):
        """Filter the files according to the patterns defined in the config files."""
        self._config = Config(self._args)
        for file_name in self._args.files:
            file_name = self._correct_path_input_file(file_name)
            self.process_file_filter_from_config(file_name)

    def _correct_path_input_file(self, file_name):
        """Expand the ~ variable and transform a relative path into an absolute one."""
        file_name = os.path.expanduser(file_name)
        file_name = os.path.abspath(file_name)
        return file_name

    def process_file_filter_from_config(self, file_name):
        """Process the file_name with the filters defined in config."""
        self._output_filter = self._config.get_filter(file_name)
        if self._output_filter:
            self.process_file(file_name)
