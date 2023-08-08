from __future__ import annotations

import typing as t

from ._serializable import Serializable

S = t.TypeVar("S", bound=Serializable)


class ValidationError(ValueError):
    pass


def str_(name: str, value: t.Any) -> str:
    if isinstance(value, str):
        return value
    raise ValidationError(f"'{name}' must be a string")


def opt_str(name: str, value: t.Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    raise ValidationError(f"'{name}' must be a string or null")


def opt_bool(name: str, value: t.Any) -> bool | None:
    if value is None or isinstance(value, bool):
        return value
    raise ValidationError(f"'{name}' must be a bool or null")


def str_list(name: str, value: t.Any) -> list[str]:
    if isinstance(value, list) and all(isinstance(s, str) for s in value):
        return value
    raise ValidationError(f"'{name}' must be a list of strings")


def opt_str_list(name: str, value: t.Any) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, list) and all(isinstance(s, str) for s in value):
        return value
    raise ValidationError(f"'{name}' must be a list of strings or null")


def opt_str_list_or_commasep(name: str, value: t.Any) -> list[str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.split(",")
    if isinstance(value, list) and all(isinstance(s, str) for s in value):
        return value
    raise ValidationError(
        f"'{name}' must be a list of strings or a comma-delimited string or null"
    )


def instance_or_dict(name: str, value: t.Any, cls: type[S]) -> S:
    if isinstance(value, cls):
        return value
    if isinstance(value, dict):
        return cls.from_dict(value)
    raise ValidationError(f"'{name}' must be a '{cls.__name__}' object or a dictionary")
