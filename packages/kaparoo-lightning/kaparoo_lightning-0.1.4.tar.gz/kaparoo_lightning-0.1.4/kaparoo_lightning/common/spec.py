# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("SpecBase", "SpecType", "update_spec")

from typing import TypedDict, TypeVar

from kaparoo.utils.optional import unwrap_or_default


class SpecBase(TypedDict, total=False):
    pass


SpecType = TypeVar("SpecType", bound=SpecBase)


def update_spec(old_spec: SpecType, new_spec: SpecType | None) -> SpecType:
    new_spec = unwrap_or_default(new_spec, {})
    return {**old_spec, **new_spec}  # type: ignore[return-value, dict-item]
