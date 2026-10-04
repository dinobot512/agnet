"""Save/load any gleeb dataclass (or list of them) as JSON. Paths ending in .gz are compressed.

Loading walks the dataclass type hints, so new schema types need no extra code. Blackboards
store their `kind` so the right subclass is rebuilt.
"""

from __future__ import annotations

import dataclasses
import gzip
import json
import types
import typing
from pathlib import Path
from typing import Any

from gleeb import __version__, schema

FORMAT = 1


def to_json(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj):
        d = {f.name: to_json(getattr(obj, f.name)) for f in dataclasses.fields(obj)}
        if isinstance(obj, schema.Blackboard):
            d["kind"] = obj.kind
        return d
    if isinstance(obj, (list, tuple)):
        return [to_json(x) for x in obj]
    if isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}
    return obj


def from_json(tp: Any, data: Any) -> Any:
    if data is None:
        return None
    origin, args = typing.get_origin(tp), typing.get_args(tp)
    if origin in (typing.Union, types.UnionType):            # X | None
        return from_json(next(a for a in args if a is not type(None)), data)
    if dataclasses.is_dataclass(tp):
        if issubclass(tp, schema.Blackboard):
            tp = schema.BOARD_TYPES[data["kind"]]
        hints = typing.get_type_hints(tp, vars(schema))
        return tp(**{f.name: from_json(hints[f.name], data[f.name])
                     for f in dataclasses.fields(tp) if f.init and f.name in data})
    if origin in (list, tuple):
        return origin(from_json(args[0], x) for x in data)
    if origin is dict:
        return {k: from_json(args[1], v) for k, v in data.items()}
    return data


def save(obj: Any, path: str | Path) -> Path:
    """Save a schema dataclass or a list of them."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    items = obj if isinstance(obj, list) else [obj]
    doc = {"gleeb_format": FORMAT, "gleeb_version": __version__,
           "type": type(items[0]).__name__ if items else "", "list": isinstance(obj, list),
           "data": to_json(obj)}
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "wt", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False)
    return path


def load(path: str | Path) -> Any:
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as f:
        doc = json.load(f)
    if doc.get("gleeb_format") != FORMAT:
        raise ValueError(f"{path}: format {doc.get('gleeb_format')}, expected {FORMAT}")
    if doc["list"] and not doc["type"]:
        return []
    tp = getattr(schema, doc["type"])
    return [from_json(tp, x) for x in doc["data"]] if doc["list"] else from_json(tp, doc["data"])
