import conf_engine.parsers.env as env


def test_get_env_var(monkeypatch):
    monkeypatch.setenv('TEST_VAR', 'test_var_value')
    assert env.EnvironmentParser().get_option_value('test_var') == 'test_var_value'


def test_get_env_group_var(monkeypatch):
    monkeypatch.setenv('TESTGROUP_TEST_VAR', 'test_var_value')
    assert env.EnvironmentParser().get_option_value('test_var', 'testgroup') == 'test_var_value'
