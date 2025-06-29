import datetime
from pathlib import Path

import pytest


@pytest.fixture(scope='session', autouse=True)
def global_init_cleanup():
    print('\n\n === GLOBAL INIT === \n\n')
    yield
    print('\n\n === GLOBAL CLEANUP === \n\n')


@pytest.fixture(scope='session')
def project_path() -> Path:
    return Path(__file__).parent.parent


@pytest.fixture(scope='session')
def sample_data_path(project_path) -> Path:
    return project_path / 'sample_data'


@pytest.fixture(scope='session')
def tests_results_path(project_path) -> Path:
    run = datetime.datetime.now().strftime('tmp_%Y-%m-%d-%H-%M-%S')
    pth = project_path / 'tests_results' / run
    pth.mkdir()
    return pth


# -----------------------------------------------------------------------------

@pytest.fixture
def sth():
    yield 'something'


# see: hhttps://docs.pytest.org/en/stable/example/simple.html#control-skipping-of-tests-according-to-command-line-option

def pytest_addoption(parser):
    parser.addoption(
        "--with-sth",
        action="store_true",
        default=False,
        help="run tests that need something",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "needs_sth: marks tests as slow"
    )


def pytest_collection_modifyitems(config, items):
    skip_needing_sth = pytest.mark.skip(reason="needs sth (--with-sth option) to run")
    for item in items:
        if "needs_sth" in item.keywords and not config.getoption("--with-sth"):
            item.add_marker(skip_needing_sth)

# -----------------------------------------------------------------------------
