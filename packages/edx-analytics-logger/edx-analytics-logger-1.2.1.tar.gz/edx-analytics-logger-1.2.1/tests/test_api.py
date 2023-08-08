from unittest import mock
from typing import Any
import pytest
import requests_mock
import sys
import os

from pytest_mock import MockFixture

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.modules["common.djangoapps.track.backends"] = mock.Mock()
sys.modules["common.djangoapps.track.utils"] = mock.Mock()

from edx_analytics_logger.api import ApiBackend, send_event_tracking_log

def test_send_event_tracking_log_success():
    # Mock the requests module to return a successful response
    http_method = "POST"
    endpoint = "https://example.com/endpoint"
    headers = {"Authorization": "Bearer ABC123"}

    with requests_mock.Mocker() as m:
        m.request(http_method, endpoint, status_code=200)
        send_event_tracking_log(http_method, "test_event", endpoint, headers)

    # Assert that the request was made
    assert len(m.request_history) == 1
    assert m.request_history[0].method == http_method
    assert m.request_history[0].url == endpoint
    assert m.request_history[0].text == "test_event"
    assert m.request_history[0].headers["Authorization"] == headers["Authorization"]

def test_send_event_tracking_log_failure(mocker: MockFixture):
    # Mock the requests module to return an error response
    http_method = "POST"
    endpoint = "https://example.com/endpoint"
    headers = {"Authorization": "Bearer ABC123"}

    mocker_log = mocker.patch("edx_analytics_logger.api.logger.exception")

    with requests_mock.Mocker() as m:
        m.request(http_method, endpoint, status_code=500, reason="Internal Server Error", text="Error Response")

        with pytest.raises(Exception) as excinfo:
            send_event_tracking_log(http_method, "test_event", endpoint, headers)

        mocker_log.assert_called_once_with("Received %s status code. Text: %s", 500, "Error Response")

