import argparse
import configparser
import os

from conf_engine.core.exceptions import ValueNotFound
from conf_engine.options import Option

class INIFileParser:
    def __init__(self, **kwargs):
        self._path_opts = self._register_paths()

    @staticmethod
    def _register_paths():
        parser = argparse.ArgumentParser()
        parser.add_argument('--config-file',
                            type=str,
                            action='append',
                            help="Configuration file path.")
        parser.add_argument('--config-dir',
                            type=str,
                            action='append',
                            help="Directory containing configuration files to be parsed.")
        args, _ = parser.parse_known_args()
        return {
            'config_files': args.config_file or [],
            'config_dirs': ['./'] if not args.config_dir and not args.config_file else args.config_dir or []
        }

    def get_option_value(self, option: Option, group: str = None):
        if not group:
            group = 'DEFAULT'
        files = self._path_opts['config_files'] + self._get_ini_files_from_dirs()
        ini_cfg = configparser.ConfigParser()
        ini_cfg.read(files)
        if group in ini_cfg and option.name in ini_cfg[group]:
            return ini_cfg[group][option.name]
        else:
            raise ValueNotFound(option)

    def _get_ini_files_from_dirs(self) -> list:
        files = []
        for directory in self._path_opts['config_dirs']:
            d = directory if directory.endswith('/') else directory + '/'
            files += [d + file for file in os.listdir(d) if file.endswith('.ini')]
        return files
