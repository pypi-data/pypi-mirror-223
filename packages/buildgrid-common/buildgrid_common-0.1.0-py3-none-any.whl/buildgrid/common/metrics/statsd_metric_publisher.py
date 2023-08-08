from contextlib import contextmanager
from datetime import timedelta
from typing import Iterator

from aio_statsd import StatsdClient

from .metric_publisher import MetricPublisher


class StatsdMetricPublisher(MetricPublisher):
    def __init__(self, statsd_client: StatsdClient, prefix: str | None = None):
        super().__init__(prefix)
        self._client = statsd_client

    @classmethod
    async def new(cls, host: str, port: int, prefix: str | None = None) -> "StatsdMetricPublisher":
        statsd_client = StatsdClient(host=host, port=port)
        publisher = cls(statsd_client, prefix)
        await publisher.connect()
        return publisher

    async def connect(self) -> None:
        await self._client.connect()

    def count(self, metric_name: str, count: int) -> None:
        self._client.counter(self._with_prefix(metric_name), count)

    def duration(self, metric_name: str, duration: timedelta) -> None:
        self._client.timer(self._with_prefix(metric_name), int(duration.total_seconds() * 1000))

    @contextmanager
    def timeit(self, metric_name: str) -> Iterator[None]:
        with self._client.timeit(self._with_prefix(metric_name)):
            yield
