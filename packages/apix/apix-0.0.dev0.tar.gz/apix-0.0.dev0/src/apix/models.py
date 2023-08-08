import typing
import msgspec
import httpx


T = typing.TypeVar("T")


def serialize(obj) -> bytes:
    """
    Serializes an object into bytes using msgspec.json encode.

    :param obj: The object to be serialized.
    :return: The serialized object as bytes.
    :rtype: bytes
    """
    return msgspec.json.encode(obj)


def deserialize(data, type_: typing.Type[T]) -> T:
    """
    Deserialize the given data into an object of the specified type.

    Args:
        data: The serialized data to be deserialized.
        type_: The type of the object to deserialize the data into.

    Returns:
        The deserialized object.
    """
    return msgspec.json.decode(data, type=type_)


class BaseObject(msgspec.Struct):
    ...


class BaseConfig(BaseObject):
    base_url: str = "https://api.example.com"


class BaseSchema(BaseObject):
    ...


class PathInfo(msgspec.Struct):
    method: str = "GET"
    path: str = "/"
    type: typing.Type[typing.Any] = bool


class BasePath(BaseObject, typing.Generic[T]):
    __info__: typing.ClassVar[PathInfo] = PathInfo()


class BaseClient:
    def __init__(self, config: typing.Optional[BaseConfig] = None):
        if isinstance(config, BaseConfig):
            self._config = config
        else:
            self._config = BaseConfig()

    @property
    def config(self) -> BaseConfig:
        return self._config

    def build_request(self, path: BasePath[T]) -> httpx.Request:
        return httpx.Request(
            method=path.__info__.method, url=self._config.base_url + path.__info__.path
        )

    def build_result(self, path: BasePath[T], response: httpx.Response) -> T:
        return deserialize(response.content, path.__info__.type)
