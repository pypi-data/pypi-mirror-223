# -*- coding: utf-8 -*-

__all__ = ("DataType", "LabelType", "TransformType", "LabelTransformType")

from collections.abc import Callable, Sequence
from typing import TypeVar

DataType = TypeVar("DataType", bound=Sequence, covariant=True)
LabelType = TypeVar("LabelType", bound=Sequence, covariant=True)

TransformType = TypeVar("TransformType", bound=Callable)
LabelTransformType = TypeVar("LabelTransformType", bound=Callable)
