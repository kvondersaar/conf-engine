import pytest

import conf_engine.configuration


@pytest.fixture
def test_ini_directory(request):
    path = ''
    for part in request.path.parts[1:]:
        path += '/' + part
        if part == 'conf_engine':
            return path + '/tests/test_ini_files'


@pytest.fixture
def test_config(monkeypatch, cli_opts: [str] = None, ):
    cli_opts = cli_opts or ['program']
    if cli_opts[0].startswith('-'):
        cli_opts.insert(0, 'program')

    monkeypatch.setattr('sys.argv', cli_opts)
    return conf_engine.configuration.Configuration()
