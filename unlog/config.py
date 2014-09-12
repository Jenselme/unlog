import glob
import configparser


class Config():
    def __init__(self, config_file):
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

    def __getitem__(self, key):
        return self._config[key]

    def __iter__(self):
        self._iter = iter(self._config)
        return self

    def __next__(self):
        return next(self._iter)
