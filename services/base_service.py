import requests
from core.config import settings
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class BaseService:
    URL: str = settings.URL
    prefix: str = ""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=5, max=15))
    def fetch_data(self, endpoint, params=None):
        try:
            logger.info(f"{self.URL}/{self.prefix}/{endpoint}")
            response = requests.get(f"{self.URL}/{self.prefix}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Fetch data error {e}")
            raise

    def post_data(self, endpoint, data):
        try:
            logger.info(f"{self.URL}/{self.prefix}/{endpoint}")
            response = requests.post(f"{self.URL}/{self.prefix}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Post data error: {e}")
            raise
