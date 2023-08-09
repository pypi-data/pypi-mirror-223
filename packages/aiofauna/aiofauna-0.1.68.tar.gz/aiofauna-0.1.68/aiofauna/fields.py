from typing import Any

from pydantic.fields import Field as F  # pylint: disable=no-name-in-module


def Field(*args, index: bool = False, unique: bool = False, **kwargs) -> Any:
    """Field Factory"""
    return F(*args, index=index, unique=unique, **kwargs)
