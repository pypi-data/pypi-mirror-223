# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("MultiDomainDataset", "DoubleDomainDataset")

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Generic, TypeVar

from torch.utils.data import Dataset

from kaparoo_lightning.common.types import TensorFn

if TYPE_CHECKING:
    from torch import Tensor
    from typing_extensions import LiteralString


DataType = TypeVar("DataType", bound=Sequence, covariant=True)
TransformType = TypeVar("TransformType", bound=Callable)


class _MultiDomainDataset(Dataset[DataType], Generic[DataType, TransformType]):
    def __init__(
        self,
        num_domains: int,
        transforms: TransformType | Sequence[TransformType | None] | None = None,
    ) -> None:
        super().__init__()
        self._transforms = self.validate_transforms(transforms, num_domains)
        self._num_domains = num_domains

    def __str__(self) -> LiteralString:
        return self.__class__.__name__

    @property
    def num_domains(self) -> int:
        return self._num_domains

    @property
    def tranforms(self) -> tuple[TransformType | None, ...]:
        return self._transforms

    @classmethod
    def validate_transforms(
        cls,
        transforms: TransformType | Sequence[TransformType | None] | None,
        max_transforms: int,
    ) -> tuple[TransformType | None, ...]:
        if not isinstance(max_transforms, int) or max_transforms < 1:
            raise ValueError(
                f"`max_transforms` must be a positive integer (got {max_transforms})"
            )

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

    @classmethod
    def apply_transforms(
        cls, transforms: Sequence[TransformType | None], domains: Sequence
    ) -> Sequence:
        if (num_domains := len(domains)) != (num_transforms := len(transforms)):
            raise ValueError(
                "`domains` and `transforms` must be the same length"
                f" (got {num_domains}, {num_transforms})"
            )

        transformed = []
        for transform, domain in zip(transforms, domains):
            transformed.append(transform(domain) if callable(transform) else domain)
        return transformed


class MultiDomainDataset(_MultiDomainDataset[tuple[Tensor, ...], TensorFn]):
    def __init__(
        self,
        num_domains: int,
        transforms: TensorFn | Sequence[TensorFn | None] | None = None,
    ) -> None:
        super().__init__(num_domains, transforms)


class DoubleDomainDataset(_MultiDomainDataset[tuple[Tensor, Tensor], TensorFn]):
    def __init__(
        self,
        transforms: TensorFn | tuple[TensorFn | None, TensorFn | None] | None = None,
    ) -> None:
        super().__init__(2, transforms)
