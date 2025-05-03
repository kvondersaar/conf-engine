import pytest

import conf_engine.parsers.ini_file as ini_file

from conf_engine.options import Option
from conf_engine.tests.conftest import test_ini_directory


def test_config_cli_args_with_no_args(monkeypatch):
    path_opts = ini_file.INIFileParser._register_paths()
    assert path_opts['config_dirs'] == ['./']
    assert path_opts['config_files'] == []


def test_config_cli_args_with_files(monkeypatch):
    monkeypatch.setattr('sys.argv', ['program', '--config-dir', '/path/one', '--config-dir', '/path/two'])
    path_opts = ini_file.INIFileParser._register_paths()
    assert path_opts['config_dirs'] == ['/path/one', '/path/two']
    assert path_opts['config_files'] == []


def test_config_cli_args_with_dirs(monkeypatch):
    monkeypatch.setattr('sys.argv', ['program', '--config-file', 'file1.ini', '--config-file', 'file2.ini'])
    path_opts = ini_file.INIFileParser._register_paths()
    assert path_opts['config_dirs'] == []
    assert path_opts['config_files'] == ['file1.ini', 'file2.ini']


def test_load_configs(monkeypatch):
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './test.ini', '--config-dir', './test_ini_files'])
    ini_file.INIFileParser()


def test_ignore_unknown_args(monkeypatch):
    monkeypatch.setattr('sys.argv', ['program', '--unknown_arg'])


@pytest.mark.parametrize('option, group, value', [
    (Option('default_option'), None, 'default_value'),
    (Option('integer'), 'numbers', '12345'),
    (Option('boolean_no'), 'booleans', 'no')
])
def test_get_config_values(option, group, value, test_ini_directory, monkeypatch):
    monkeypatch.chdir(test_ini_directory)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './test.ini', '--config-dir', './types'])
    ifp = ini_file.INIFileParser()
    assert ifp.get_option_value(option, group) == value