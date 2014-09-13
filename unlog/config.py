import glob
import os
import configparser

try:
    from filter import Filter
except ImportError:
    from unlog.filter import Filter


class Config():
    CONFIG_FILTER_KEYS_EXCLUDED = ['files', 'config_file', 'use_config_section']

    def __init__(self, command_line_args):
        self._args = command_line_args  # Used to override the necessary variable
        config_file = self._args.config_file
        self._use_config_section = self._args.use_config_section
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

    def __getitem__(self, key):
        return self._config[key]

    def get_filter(self, section_name=''):
        """Returns the Filter association with the asked section if it exits."""
        config_section = self._get_config_section(section_name)
        if config_section:
            config_filter = self._get_config_filter(config_section)
            return Filter(**config_filter)

    def _get_config_section(self, section_name):
        """Returns the name of the config_section and takes into account ~ ($HOME)
        and blobs.
        """
        if self._use_config_section:
            return self._use_config_section

        for config_section in self._config:
            config_section_user_expanded = os.path.expanduser(config_section)
            possible_section_names = glob.glob(config_section_user_expanded)
            if section_name in possible_section_names:
                return config_section

    def _get_config_filter(self, config_section):
        """Returns a dict containing the config for the Filter.
        
        Key of the in _config sections contains spaces. We need to replace them
        with _ in order to pass the dict to the constructor of Filter so that
        named argument correctly match.
        """
        config = self._config[config_section]
        config_filter = dict()
        for key, item in config.items():
            new_key = key.replace(' ', '_')
            config_filter[new_key] = item

        for key, item in self._args.__dict__.items():
            if item is not None and key not in self.CONFIG_FILTER_KEYS_EXCLUDED:
                config_filter[key] = item

        return config_filter
