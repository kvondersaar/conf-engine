import pytest


def test_register_option(test_ini_directory, test_config, monkeypatch):
    from conf_engine.options import StringOption

    opt = StringOption('default_option')
    test_config.register_option(opt)
    assert test_config._group_cache[None]._opt_cache[opt.name] is opt


def test_register_options(test_ini_directory, test_config, monkeypatch):
    from conf_engine.options import Option

    options = [Option(opt_name) for opt_name in ['option1', 'option2', 'option3']]
    test_config.register_options(options)
    for option in options:
        assert test_config._group_cache[None]._opt_cache[option.name] is option


def test_register_options_in_group(test_ini_directory, test_config, monkeypatch):
    from conf_engine.options import Option

    options = [Option(opt_name) for opt_name in ['option1', 'option2', 'option3']]
    test_config.register_options(options, 'opt_group')
    for option in options:
        assert test_config._group_cache['opt_group']._opt_cache[option.name] is option



def test_register_same_option_name_with_different_params(test_config):
    from conf_engine.options import StringOption, NumberOption
    from conf_engine.core.exceptions import DuplicateOptionError

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
        StringOption('test_none_default_option', default=None)
    ]
    test_config.register_options(options)
    assert test_config.test_bool_option
    assert not test_config.test_bool_false_option
    assert test_config.default_option == 'default_value'
    assert test_config.test_option_default == 100
    assert test_config.test_none_default_option is None


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


@pytest.mark.parametrize('test_env, test_group, test_expression', [
    ('TESTNS_TEST_VAR', None, 'config.test_var'),
    ('TESTNS_TEST_GROUP_TEST_VAR', 'test_group', 'config.test_group.test_var')
])
def test_custom_config_namespace(test_env, test_group,
                                 test_expression, monkeypatch):
    monkeypatch.setenv(test_env, 'test_value')
    from conf_engine import Configuration
    from conf_engine.options import StringOption
    config = Configuration(namespace='testns')
    config.register_option(StringOption('test_var'), group=test_group)
    value = eval(test_expression)
    assert value == 'test_value'

@pytest.mark.parametrize('test_option, test_group', [
    ('my_option', None),
    ('my_option', 'my_group')
])
def test_value_not_found(test_option, test_group):
    from conf_engine import config, options
    from conf_engine.core.exceptions import ValueNotFound
    config.register_option(options.StringOption(test_option), test_group)
    with pytest.raises(ValueNotFound):
        if test_group:
            getattr(getattr(config, test_group), test_option)
        else:
            getattr(config, test_option)
