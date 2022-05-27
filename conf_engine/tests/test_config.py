import pytest


def test_register_option(test_ini_directory, test_config, monkeypatch):
    monkeypatch.chdir(test_ini_directory)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './test.ini'])
    from conf_engine.options import StringOption

    test_config.register_option(StringOption('default_option'))
    assert test_config.default_option == 'default_value'


def test_register_options(test_ini_directory, test_config, monkeypatch):
    monkeypatch.chdir(test_ini_directory)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './test.ini'])

    from conf_engine.options import StringOption, NumberOption
    options = [
        StringOption('default_option'),
        StringOption('test_option_two'),
        NumberOption('test_int'),
    ]
    test_config.register_options(options)
    assert test_config.default_option == 'default_value'
    assert test_config.test_option_two == 'test_two'
    assert test_config.test_int == 12345


def test_register_options_in_group(test_ini_directory, test_config, monkeypatch):
    monkeypatch.chdir(test_ini_directory)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './types/booleans.ini'])

    from conf_engine.options import BooleanOption
    options = [
        BooleanOption('boolean_true'),
        BooleanOption('boolean_yes'),
        BooleanOption('boolean_false'),
        BooleanOption('boolean_no')
    ]
    test_config.register_options(options, 'booleans')
    assert test_config.booleans.boolean_true
    assert test_config.booleans.boolean_yes
    assert not test_config.booleans.boolean_false
    assert not test_config.booleans.boolean_no


def test_register_same_option_name_with_different_params(test_config):
    from conf_engine.options import StringOption, NumberOption
    from conf_engine.exceptions import DuplicateOptionError

    test_config.register_option(StringOption('default_option'))
    with pytest.raises(DuplicateOptionError):
        test_config.register_option(NumberOption('default_option'))


def test_register_same_option_name_with_same_params(test_config):
    from conf_engine.options import StringOption

    test_config.register_option(StringOption('default_option'))
    test_config.register_option(StringOption('default_option'))


def test_default_options(test_ini_directory, test_config, monkeypatch):
    monkeypatch.chdir(test_ini_directory)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './test.ini'])

    from conf_engine.options import BooleanOption, NumberOption, StringOption
    options = [
        StringOption('default_option', default='This should not return the default.'),
        NumberOption('test_option_default', default=100),
        BooleanOption('test_bool_option', default=True),
        BooleanOption('test_bool_false_option', default=False),
    ]
    test_config.register_options(options)
    assert test_config.test_bool_option
    assert not test_config.test_bool_false_option
    assert test_config.default_option == 'default_value'
    assert test_config.test_option_default == 100


def test_option_precedence(test_ini_directory, test_config, monkeypatch):
    monkeypatch.chdir(test_ini_directory)
    monkeypatch.setattr('sys.argv', ['program', '--config-file', './test.ini'])
    monkeypatch.setenv('DEFAULT_OPTION', 'env_value')

    from conf_engine.options import StringOption
    options = [
        StringOption('default_option', default='This should not return the default.')
    ]
    test_config.register_options(options)
    assert test_config.default_option == 'env_value'


def test_option_value_caching(test_config, monkeypatch):
    monkeypatch.setenv('DEFAULT_OPTION', 'env_value')
    from conf_engine.options import StringOption
    options = [
        StringOption('default_option', default='This should not return the default.')
    ]
    test_config.register_options(options)
    assert not test_config._get_group(None)._option_value_cached('default_option')
    _ = test_config.default_option
    assert test_config._get_group(None)._option_value_cached('default_option')
    assert test_config._get_group(None)._get_option_value_from_cache('default_option') == 'env_value'


def test_option_value_cache_flush(test_config, monkeypatch):
    monkeypatch.setenv('OPG_STR_OPTION', 'opt_value')
    from conf_engine.options import StringOption
    options = [
        StringOption('str_option')
    ]
    test_config.register_options(options, 'opg')
    assert not test_config._get_group('opg')._option_value_cached('str_option')
    _ = test_config.opg.str_option
    assert test_config._get_group('opg')._option_value_cached('str_option')
    test_config.flush_cache()
    assert not test_config._get_group('opg')._option_value_cached('str_option')
    _ = test_config.opg.str_option
    assert test_config._get_group('opg')._option_value_cached('str_option')
