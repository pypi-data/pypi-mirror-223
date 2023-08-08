from __future__ import annotations

import enum
from abc import abstractmethod
from collections.abc import Iterable, Collection, Sized, Iterator
from typing import Any, Optional, Protocol, TypeVar


class MyMeta(type): # implements Iterable[str] and Sized, however explicit subclassing breaks pandas isinstance checks
    def __new__(cls, name, bases, dct):
        cli = super().__new__(cls, name, bases, dct)
        cli.value_map = {k: v for k, v in dct.items() if not str.startswith(k, '_') and type(v) is str}
        cli.values = list(cli.value_map.values())
        return cli

    def __getitem__(self, key) -> str:
        if key in self.value_map:
            return self.value_map[key]
        elif key in self.values:
            return key

    def __len__(self) -> int:
        return len(self.value_map)

    def __iter__(self) -> Iterator[str]:
        return iter(self.values)

    def derive_enum(cls, name=None):
        return enum.Enum(cls.__name__[:-1] if name is None else name, cls.value_map)


class StringEnumeration(metaclass=MyMeta):
    pass


K = TypeVar('K')
V = TypeVar('V', covariant=True)


class SlimMapping(Sized, Iterable[V], Protocol[K, V]):
    @abstractmethod
    def __contains__(self, __x: object) -> bool: ...

    @abstractmethod
    def __getitem__(self, item: K) -> V:  ...


def take_first(arg: Iterable[Any]) -> Optional[Any]:
    return next(iter(arg), None)


def intersection(a, b) -> set:
    if a is None or b is None:
        return set()
    else:
        return set(a) & set(b)


def symmetric_difference(a, b) -> tuple[set, set]:
    if a is None and b is None:
        return set(), set()
    elif a is None:
        return set(), set(b)
    elif b is None:
        return set(a), set()
    else:
        a, b = set(a), set(b)
        return a - b, b - a


def mangle_arg_to(arg: None | str | Iterable, cls, rm_duplicates=False, preserve_order=True, preserve_none=False):
    if arg is None:
        return arg if preserve_none else cls()
    elif not type(arg) is str and isinstance(arg, Iterable):
        if rm_duplicates:
            if not preserve_order:
                return cls(set(arg))
            elif preserve_order:
                s = set()
                return cls(
                    (i for i in arg if (i not in s) and (s := s | {i})))  # the things I do for an (almost) one-liner
        else:
            return cls(arg)
    else:
        return cls((arg,))


def mangle_arg_to_set(arg, **kwargs):
    return mangle_arg_to(arg, set, **kwargs)


def mangle_arg_to_list(arg, rm_duplicates=True, preserve_order=True, **kwargs):
    return mangle_arg_to(arg, list, rm_duplicates=rm_duplicates, preserve_order=preserve_order, **kwargs)


def mangle_arg_to_tuple(arg, rm_duplicates=True, preserve_order=True, **kwargs):
    return mangle_arg_to(arg, tuple, rm_duplicates=rm_duplicates, preserve_order=preserve_order, **kwargs)


def assert_in(items: Iterable, allowed: Collection):
    assert all(i in allowed for i in items)


def mangle_arg_with_bool_fallback(mangler, arg, if_true=None, if_false=None, treat_none_as_false=True, **kwargs):
    if arg is None and treat_none_as_false:
        arg = if_false
    elif isinstance(arg, bool):
        arg = if_true if arg else if_false
    return mangler(arg, **kwargs)
