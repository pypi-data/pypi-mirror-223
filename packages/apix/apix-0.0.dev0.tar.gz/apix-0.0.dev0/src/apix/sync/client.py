import typing
import httpx

from ..models import BaseClient, BaseConfig, BasePath, T


class BaseSyncClient(BaseClient):
    def __init__(self, config: typing.Optional[BaseConfig] = None):
        super().__init__(config)
        self._http = httpx.Client()

    def __call__(self, path: BasePath[T]) -> T:
        return self.build_result(path, self._http.send(self.build_request(path)))
