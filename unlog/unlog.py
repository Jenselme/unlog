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
    """Filter the output of a command or a log file according to pattern passed
    in the *args* argument or according to a config file.
    """

    def __init__(self, args):
        """    **PARAMETERS**

        * *args* - an ArgumentParser object containing all the option. Look at
          :py:mod:`unlog.main` for the list of opitons.
      """
        self._args = args
        self._check_args()
        if args.start_pattern:
            self._filter_from_args()
        else:
            self._filter_from_config()

    def _check_args(self):
        """Verify that the arguments are coherent. Exit with error code 2 if
        incoherences are fonud.
        """
        if not self._args.files and not self._args.start_pattern \
        and not self._args.use_config_section:
            sys.stderr.write('You must give a file or a start pattern.\n')
            sys.exit(2)
        if (self._args.start_group_pattern and not self._args.end_group_pattern)\
        or (not self._args.start_group_pattern and self._args.end_group_pattern):
            sys.stderr.write('You must --start-group and --end-group.')
            sys.exit(2)

    def _filter_from_args(self):
        """Filter the files or stdin according to the patterns give by the
        arguments provided on the command line.
        """
        config = copy.copy(self._args.__dict__)
        # Must not be passed to filter (unuseful)
        del config['files']
        # The following key are only used when processing from a config file
        del config['config_file']
        del config['use_config_section']
        # The filter manipulates string in the proper encoding. No need to pass it.
        del config['log_encoding']
        self._output_filter = Filter(**config)
        # If no files are provided, read from stdin
        if self._args.files:
            self._files = self._args.files
            self.process_files()
        else:
            self.process_stdin()

    def process_files(self):
        """Loop on each file given on the command line and process them.
        """
        for file in self._files:
            self.process_file(file, log_encoding=self._args.log_encoding)

    def process_file(self, file_name, log_encoding='utf-8'):
        """Open file_name and process it with :py:meth:`unlog.filter.Filter.process_file`
        """
        try:
            with open(file_name, 'r', encoding=log_encoding) as file:
                self._output_filter.process_file(file)
        except IOError as e:
            sys.stderr.write(str(e))
            sys.stderr.write("\n")

    def process_stdin(self):
        """Process each line on the stdin with
        :py:meth:`unlog.filter.Filter.process_line`
        """
        for line in iter(sys.stdin.readline, ''):
            self._output_filter.process_line(line)
        # We must print the stack when we reach the last line of stdin so that the
        # errors located at the end are displayed.
        self._output_filter.print_stack()
        self._output_filter.send_mail()

    def _filter_from_config(self):
        """Filter the files according to the patterns defined in the
        configuration file.
        """
        self._config = Config(self._args)
        if self._args.files:
            self.process_files_from_config()
        else:
            self._output_filter = self._config.get_filter()
            self.process_stdin()

    def process_files_from_config(self):
        """Loop over each file given on the command line and process them
        according to the actions defined in the associated config file. The file
        is then passed to :py:meth:`process_file_filter_from_config`.
        """
        for file_name in self._args.files:
            file_name = self._correct_path_input_file(file_name)
            self.process_file_filter_from_config(file_name)

    def _correct_path_input_file(self, file_name):
        """Expand the ~ variable and transform a relative path into an absolute
        one.
        """
        file_name = os.path.expanduser(file_name)
        file_name = os.path.abspath(file_name)
        return file_name

    def process_file_filter_from_config(self, file_name):
        """Process the file_name with the filters defined in config with
        :py:meth:`process_file`.
        """
        self._output_filter = self._config.get_filter(file_name)
        if self._output_filter:
            if 'encoding' in self._config:
                self.process_file(file_name, log_encoding=self._config['encoding'])
            else:
                self.process_file(file_name)
