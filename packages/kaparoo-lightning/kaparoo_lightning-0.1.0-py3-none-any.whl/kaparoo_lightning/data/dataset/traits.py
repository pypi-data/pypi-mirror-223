# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("MultiDomain", "MultiLabeled")

from collections.abc import Sequence
from typing import TYPE_CHECKING, Generic

if TYPE_CHECKING:
    from kaparoo_lightning.data.dataset.types import DataType, LabelType, TransformType


def unwrap_transforms(
    transforms: TransformType | Sequence[TransformType | None] | None,
    max_transforms: int,
) -> tuple[TransformType | None, ...]:
    if not isinstance(max_transforms, int) or max_transforms < 1:
        raise ValueError(f"`max_transforms` must a positive int (got {max_transforms})")

    def duplicate(
        transform: TransformType | None, length: int = max_transforms
    ) -> Sequence[TransformType | None]:
        return [transform] * length

    if isinstance(transforms, Sequence):
        if (num_transforms := len(transforms)) == 0:
            transforms = duplicate(None)
        elif num_transforms == 1:
            transforms = duplicate(transforms[0])
        elif num_transforms < max_transforms:
            padding = duplicate(None, max_transforms - num_transforms)
            transforms = [*transforms, *padding]
        elif num_transforms > max_transforms:
            transforms = transforms[:max_transforms]
    else:
        transforms = duplicate(transforms)

    return tuple(transforms)


class MultiDomain(Generic[DataType, TransformType]):
    def __init__(
        self,
        num_domains: int,
        transforms: TransformType | Sequence[TransformType | None] | None = None,
    ) -> None:
        if not isinstance(num_domains, int) or num_domains < 1:
            raise ValueError(f"`num_domains` must a positive int (got {num_domains})")

        self._num_domains = num_domains
        self._transforms = unwrap_transforms(transforms, num_domains)

    @property
    def num_domains(self) -> int:
        return self._num_domains

    @property
    def transforms(self) -> tuple[TransformType | None, ...]:
        return self._transforms


class MultiLabeled(Generic[LabelType, TransformType]):
    def __init__(
        self,
        num_labels: int,
        label_transforms: TransformType | Sequence[TransformType | None] | None = None,
    ) -> None:
        if not isinstance(num_labels, int) or num_labels < 1:
            raise ValueError(f"`num_labels` must a positive int (got {num_labels})")

        self._num_labels = num_labels
        self._label_transforms = unwrap_transforms(label_transforms, num_labels)

    @property
    def num_labels(self) -> int:
        return self._num_labels

    @property
    def label_transforms(self) -> tuple[TransformType | None, ...]:
        return self._label_transforms
