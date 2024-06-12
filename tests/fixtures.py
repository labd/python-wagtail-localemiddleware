import pytest
import requests_mock


@pytest.fixture
def requests_mocker():
    """Allow mocking a request."""
    with requests_mock.Mocker() as m:
        yield m
