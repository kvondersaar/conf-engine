import pytest

import conf_engine.parsers.cli as cli


@pytest.mark.parametrize('test_opt, test_group, test_ns', [
    ('test-var', None, None),
    ('testgroup-test-var', 'testgroup', None),
    ('test-group-test-var', 'test_group', None),
    ('testns-test-var', None, 'testns'),
    ('testns-testgroup-test-var', 'testgroup', 'testns'),
    ('testns-test-group-test-var', 'test_group', 'testns'),
])
def test_get_cli_var(test_opt, test_group, test_ns, monkeypatch):
    import sys
    from conf_engine.options import Option
    option = Option('test_var')
    test_value = 'test_value'
    add_argv = [f'--{test_opt}', test_value]
    monkeypatch.setattr(sys, 'argv', sys.argv + add_argv)

    parser = cli.CLIParser(namespace=test_ns)
    value = parser.get_option_value(option, test_group)

    assert value == test_value


@pytest.mark.parametrize('flag, add_argv, expected', [
    (True, ['--test-flag'], True),
    (False, ['--test-flag', 'yes'], 'yes'),
    (True, [], False),
    (False, ['--test-flag', 'no'], 'no'),
    (True, ['--test-flag', '--extra-flag'], True),
    (False, ['--test-flag', 'yes', '--extra-flag'], 'yes'),
    (True, ['--extra-flag'], False),
    (False, ['--test-flag', 'no', '--extra-flag'], 'no'),
    (True, ['--extra-flag', '--test-flag'], True),
    (False, ['--extra-flag', '--test-flag', 'yes'], 'yes'),
    (False, ['--extra-flag', '--test-flag', 'no'], 'no')
    ])
def test_get_cli_boolean(flag, add_argv, expected, monkeypatch):
    import sys
    from conf_engine.options import BooleanOption
    option = BooleanOption('test_flag', flag=flag)

    monkeypatch.setattr(sys, 'argv', sys.argv + add_argv)

    parser = cli.CLIParser()

    assert parser.get_option_value(option) == expected

@pytest.mark.parametrize('add_argv', [[], ['--test-option']])
def test_get_cli_missing_value(add_argv, monkeypatch):
    import sys
    from conf_engine.options import Option
    from conf_engine.core.exceptions import ValueNotFound
    option = Option('test_option')

    monkeypatch.setattr(sys, 'argv', sys.argv + add_argv)
    parser = cli.CLIParser()
    with pytest.raises(ValueNotFound):
        parser.get_option_value(option)