import requests
import time
from logging import getLogger
logger = getLogger(__name__)


class RequestLogger(requests.Session):
    default_timeout = 15

    def request(self, method, url, *args, **kwargs):
        start_time = time.time()
        response = None
        kwargs.setdefault('timeout', self.default_timeout)
        try:
            response = super().request(method, url, *args, **kwargs)
        finally:
            elapsed = time.time() - start_time
            status = response.status_code
            logger.info(f'{method} {url} {status} {elapsed:0.3f}')
        return response
