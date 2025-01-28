from collections.abc import Callable
from functools import lru_cache

from aquant_sdk.api.base.interfaces import HTTPClientInterface
from aquant_sdk.settings import settings


def lru_cache_wrapper(maxsize: int = 1000) -> Callable:
    return lru_cache(maxsize=maxsize)


class BrokerService:
    def __init__(self, http_client: HTTPClientInterface) -> None:
        self.http_client = http_client
        self._get_brokers_name_cached = lru_cache_wrapper()(self._fetch_broker_name)

    async def get_brokers_name(self, broker_id: int) -> str:
        return await self._get_brokers_name_cached(broker_id)

    async def _fetch_broker_name(self, broker_id: int) -> str:
        try:
            url = f"{settings.BROKER_API}/{broker_id}"
            response = await self.http_client.get(url)

            if response.status_code == 200:
                data = response.json()
                return data.get("name", "Name not found")
            else:
                return f"Error: {response.status_code} - {response.text}"

        except Exception as exc:
            self.http_client.logger.error(f"Failed to fetch broker {broker_id}: {exc}")
            return "Error fetching broker name"
