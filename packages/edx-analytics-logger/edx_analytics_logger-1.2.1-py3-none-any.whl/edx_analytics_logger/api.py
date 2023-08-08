"""Api Analytics event tracker backend.
"""
import json
import logging
import requests

from celery import shared_task
from common.djangoapps.track.backends import BaseBackend
from common.djangoapps.track.utils import DateTimeJSONEncoder
from typing import Any

logger = logging.getLogger(__name__)


@shared_task
def send_event_tracking_log(http_method: str, event_str: str, endpoint: str, headers: dict) -> None:
    r = requests.request(http_method, endpoint, data=event_str, headers=headers)
    try:
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.exception("Received %s status code. Text: %s", r.status_code, r.text)
        raise e
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        raise e


class ApiBackend(BaseBackend):

    def __init__(self, http_method: str, endpoint: str, headers: dict, **kwargs) -> None:
        """Event tracker backend to send payloads to a remote endpoint.
        :Parameters:
          - `http_method`: HTTP Method used by the outgoing request.
          - `endpoint`: URI endpoint which should receive the event.
          - `headers`: Dictionary containing required headers to authenticate against defined API.
        """
        self.http_method = http_method
        self.endpoint = endpoint
        self.headers = headers
        super().__init__(**kwargs)

    def send(self, event: Any) -> None:
        event_str = json.dumps(event, cls=DateTimeJSONEncoder)
        send_event_tracking_log.delay(self.http_method, event_str, self.endpoint, self.headers)
