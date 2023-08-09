"""
Tests that version number has increased from PyPI-deployed version.
"""

import importlib
import sys
from os import environ as env
from pathlib import Path

import pytest
import requests

import localeet
from localeet.get_version import get_version

from conftest import MockValue


RUNNING_LOCALLY = env.get('CI') is None and env.get('PRE_COMMIT') is None
SKIP_REASON = """
Version number must be updated prior to deploying a
new version to PyPI. Run this test when committing
new code and in CI, but don't run on a simple call
of `pytest tests`, as tests should pass by default
when pulling down the latest version.
"""


@pytest.mark.skipif(RUNNING_LOCALLY, reason=SKIP_REASON)
def test_version_has_been_updated() -> None:
    """Ensure latest version is greater than latest published version"""
    pypi_version = get_pypi_version()
    # add local repo to path to ensure we get local version
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    importlib.reload(localeet)
    assert localeet.__version__ > pypi_version


def test_get_version(any_version: MockValue) -> None:
    assert get_version() == any_version


def get_pypi_version() -> str:
    """Return latest localeet version published to PyPI"""
    try:
        pypi_url = 'https://pypi.org/pypi/localeet/json'
        response = requests.get(pypi_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data['info']['version']
    except requests.RequestException:
        raise
