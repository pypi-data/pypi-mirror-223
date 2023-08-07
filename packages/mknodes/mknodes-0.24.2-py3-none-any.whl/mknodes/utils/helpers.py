from __future__ import annotations

from collections.abc import Callable
import contextlib
import functools

from importlib import metadata
import inspect
import itertools
import logging
import os
import re
import reprlib
import sys
import types
from typing import Any


logger = logging.getLogger(__name__)

BASE_URL = "https://doc.qt.io/qtforpython-6/PySide6/"
BUILTIN_URL = "https://docs.python.org/3/library/{mod}.html#{name}"


class LengthLimitRepr(reprlib.Repr):
    def repr_type(self, obj, level):
        return obj.__name__

    def repr_module(self, obj, level):
        return obj.__name__

    def repr_function(self, obj, level):
        return obj.__name__


limit_repr = LengthLimitRepr()
limit_repr.maxlist = 10
limit_repr.maxstring = 80


@contextlib.contextmanager
def new_cd(x):
    d = os.getcwd()  # noqa: PTH109
    os.chdir(x)
    yield
    os.chdir(d)


def get_repr(
    _obj: Any,
    *args: Any,
    _shorten: bool = True,
    _filter_empty: bool = False,
    _filter_false: bool = False,
    **kwargs: Any,
) -> str:
    """Get a suitable __repr__ string for an object.

    Args:
        _obj: The object to get a repr for.
        _shorten: Whether to shorten the repr.
        *args: Arguments for the repr
        **kwargs: Keyword arguments for the repr
    """
    my_repr = limit_repr.repr if _shorten else repr
    classname = type(_obj).__name__
    parts = [my_repr(val) for val in args]
    kw_parts = []
    for k, v in kwargs.items():
        if _filter_empty and (v is None or v == "" or v == {}):
            continue
        if _filter_false and v is False:
            continue
        name = my_repr(v)
        kw_parts.append(f"{k}={name}")
    sig = ", ".join(parts + kw_parts)
    return f"{classname}({sig})"


def escaped(text: str, entity_type: str | None = None) -> str:
    """Helper function to escape markup.

    Args:
        text: The text.
        entity_type: For the entity types ``PRE``, ``CODE`` and the link
                     part of ``TEXT_LINKS``, only certain characters need to be escaped.
    """
    if entity_type in ["pre", "code"]:
        escape_chars = r"\`"
    elif entity_type == "text_link":
        escape_chars = r"\)"
    else:
        escape_chars = r"_*[]()~`>#+-=|{}.!"

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub("[^0-9a-zA-Z_.]", "_", text)
    return re.sub("^[^a-zA-Z_#]+", "", text)


def groupby(data, keyfunc: Callable | None = None) -> dict[str, list]:
    data = sorted(data, key=keyfunc or (lambda x: x))
    return {k: list(g) for k, g in itertools.groupby(data, keyfunc)}


def groupby_first_letter(data, keyfunc: Callable | None = None) -> dict[str, list]:
    data = sorted(data, key=keyfunc or (lambda x: x))

    def first_letter(x):
        return keyfunc(x)[0] if keyfunc else x[0]

    return {k: list(g) for k, g in itertools.groupby(data, first_letter)}


def linked(identifier: str, title: str | None = None) -> str:
    suffix = (
        ""
        if identifier.startswith(("http:", "https:", "www."))
        or identifier.endswith(".md")
        else ".md"
    )
    return f"[{identifier if title is None else title}]({identifier}{suffix})"


def styled(
    text: str,
    *,
    size: int | None = None,
    bold: bool = False,
    recursive: bool = False,
    code: bool = False,
) -> str:
    if size:
        text = f"<font size='{size}'>{text}</font>"
    if bold:
        text = f"**{text}**"
    if recursive:
        text = f"*{text}*"
    if code:
        text = f"`{text}`"
    return text


def link_for_class(kls: type, **kwargs) -> str:
    if kls.__module__ == "builtins":
        url = BUILTIN_URL.format(mod="functions", name=kls.__name__)
        link = linked(url, title=kls.__name__)
    elif kls.__module__ in sys.stdlib_module_names:
        mod = kls.__module__
        url = BUILTIN_URL.format(mod=mod, name=f"{mod}.{kls.__name__}")
        link = linked(url, title=kls.__name__)
    elif kls.__module__.startswith(("PyQt", "PySide")):
        mod = kls.__module__.replace("PySide6.", "").replace("PyQt6.", "")
        url = f"{BASE_URL}{mod}/{kls.__qualname__.replace('.', '/')}.html"
        link = linked(url, title=kls.__name__)
    elif kls.__module__.startswith("prettyqt"):
        link = linked(kls.__qualname__)
    else:
        module = kls.__module__.split(".")[0]
        qual_name = kls.__qualname__.split("[")[0]  # to split off generics part
        if url := homepage_for_distro(module):
            link = linked(url, title=qual_name)
        else:
            link = linked(qual_name)
    return styled(link, **kwargs)


@functools.cache
def homepage_for_distro(dist_name: str):
    try:
        dist = metadata.distribution(dist_name)
    except metadata.PackageNotFoundError:
        return None
    else:
        return dist.metadata["Home-Page"]


def label_for_class(klass: type) -> str:
    if klass.__module__.startswith("prettyqt."):
        parts = klass.__module__.split(".")
        return f"{parts[1]}.{klass.__name__}"
    return f"{klass.__module__.split('.')[-1]}.{klass.__name__}"


def to_html_list(
    ls: list[str],
    *,
    shorten_after: int | None = None,
    make_link: bool = False,
) -> str:
    if not ls:
        return ""
    item_str = "".join(
        f"<li>{linked(i)}</li>" if make_link else f"<li>{i}</li>"
        for i in ls[:shorten_after]
    )
    if shorten_after and len(ls) > shorten_after:
        item_str += "<li>...</li>"
    return f"<ul>{item_str}</ul>"


@functools.cache
def get_function_body(func: types.MethodType | types.FunctionType | type) -> str:
    # see https://stackoverflow.com/questions/38050649
    source_lines, _ = get_source_lines(func)
    source_lines = itertools.dropwhile(lambda x: x.strip().startswith("@"), source_lines)
    line = next(source_lines).strip()  # type: ignore
    if not line.startswith(("def ", "class ")):
        return line.rsplit(":")[-1].strip()
    if not line.endswith(":"):
        for line in source_lines:
            line = line.strip()
            if line.endswith(":"):
                break
    return "".join(source_lines)


def get_deprecated_message(obj) -> str | None:
    return obj.__deprecated__ if hasattr(obj, "__deprecated__") else None


@functools.cache
def get_doc(
    obj,
    *,
    escape: bool = False,
    fallback: str = "",
    from_base_classes: bool = False,
    only_summary: bool = False,
) -> str:
    if from_base_classes:
        doc = inspect.getdoc(obj)
    else:
        doc = inspect.cleandoc(obj.__doc__) if isinstance(obj.__doc__, str) else None
    if not doc:
        return fallback
    if only_summary:
        doc = doc.split("\n")[0]
    return escaped(doc) if doc and escape else doc


@functools.cache
def get_source(obj):
    return inspect.getsource(obj)


@functools.cache
def get_source_lines(obj):
    return inspect.getsourcelines(obj)


@functools.cache
def get_file(klass: type) -> str | None:
    with contextlib.suppress(TypeError):
        return inspect.getfile(klass)
    return None


if __name__ == "__main__":
    strings = groupby_first_letter([str(i) for i in range(1000)])
    print(limit_repr.repr(strings))
