from abc import ABC, abstractmethod
from typing import (Any, Dict, Generic, Iterable, List, Type, TypeVar, Union,
                    cast)

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from .utils import handle_errors, setup_logging, timer

Vector = List[float]
MetaData = Dict[str, str]

logger = setup_logging(__name__)

T = TypeVar("T")


class LazyProxy(Generic[T], ABC):
    def __init__(self) -> None:
        self.__proxied: Union[T, None] = None

    def __getattr__(self, attr: str) -> object:
        return getattr(self.__get_proxied__(), attr)

    def __repr__(self) -> str:
        return repr(self.__get_proxied__())

    def __dir__(self) -> Iterable[str]:
        return self.__get_proxied__().__dir__()

    def __get_proxied__(self) -> T:
        proxied = self.__proxied
        if proxied is not None:
            return proxied

        self.__proxied = proxied = self.__load__()
        return proxied

    def __set_proxied__(self, value: T) -> None:
        self.__proxied = value

    def __as_proxied__(self) -> T:
        """Helper method that returns the current proxy, typed as the loaded object"""
        return cast(T, self)

    @abstractmethod
    def __load__(self) -> T:
        ...


class FunctionCall(BaseModel):
    name: str
    data: Any


class FunctionType(BaseModel, ABC):
    _subclasses: List[Type["FunctionType"]] = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        logger.debug("OpenAI Function %s called", self.__class__.__name__)

    @classmethod
    def __init_subclass__(cls, **kwargs:Any):
        super().__init_subclass__(**kwargs)
        _schema = cls.schema()
        if cls.__doc__ is None:
            raise ValueError(
                f"FunctionType subclass {cls.__name__} must have a docstring"
            )
        cls.openaischema = {
            "name": cls.__name__,
            "description": cls.__doc__,
            "parameters": {
                "type": "object",
                "properties": _schema["propertites"],
                "required": _schema["required"],
            },
        }
        cls._subclasses.append(cls)

    @timer
    @handle_errors
    async def __call__(self, **kwargs:Any) -> FunctionCall:
        response = await self.run(**kwargs)
        name = self.__class__.__name__
        return FunctionCall(name=name, data=response)

    @abstractmethod
    async def run(self, **kwargs:Any) -> Any:
        ...


F = TypeVar("F", bound=FunctionType)
