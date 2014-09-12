import glob
import os
import configparser
try:
    from filter import Filter
except ImportError:
    from unlog.filter import Filter


class Config():
    def __init__(self, config_file):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

    def __getitem__(self, key):
        return self._config[key]

    def get_filter(self, section_name):
        """Returns the Filter association with the asked section if it exits."""
        config_section = self._get_config_section(section_name)
        if config_section:
            return Filter(error_pattern=self._config[config_section]['error pattern'],
                          start_pattern=self._config[config_section]['start pattern'])

    def _get_config_section(self, section_name):
        """Returns the name of the config_section and takes into account ~ ($HOME)
        and blobs.
        """
        for config_section in self._config:
            config_section_user_expanded = os.path.expanduser(config_section)
            possible_section_names = glob.glob(config_section_user_expanded)
            if section_name in possible_section_names:
                return config_section
