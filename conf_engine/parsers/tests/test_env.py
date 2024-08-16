import pytest

import conf_engine.parsers.env as env


@pytest.mark.parametrize('test_env, test_group, test_ns', [
    ('TEST_VAR', None, None),
    ('TESTGROUP_TEST_VAR', 'testgroup', None),
    ('TEST_GROUP_TEST_VAR', 'test_group', None),
    ('TESTNS_TEST_VAR', None, 'testns'),
    ('TESTNS_TESTGROUP_TEST_VAR', 'testgroup', 'testns'),
    ('TESTNS_TEST_GROUP_TEST_VAR', 'test_group', 'testns'),
])
def test_get_env_var(test_env, test_group, test_ns, monkeypatch):
    from conf_engine.options import Option
    option = Option('test_var')
    monkeypatch.setenv(test_env, 'test_value')
    parser = env.EnvironmentParser(namespace=test_ns)
    value = parser.get_option_value(option, test_group)
    assert value == 'test_value'
