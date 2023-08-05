# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("MultiDomainDataset", "DoubleDomainDataset")

from typing import TYPE_CHECKING, Generic

from torch.utils.data import Dataset

from kaparoo_lightning.data.datasets.traits import MultiDomain

if TYPE_CHECKING:
    from collections.abc import Sequence

    from torch import Tensor
    from typing_extensions import LiteralString

    from kaparoo_lightning.common.types import TensorFn
    from kaparoo_lightning.data.datasets.types import DataType, TransformType


class _MultiDomainDataset(
    MultiDomain[DataType, TransformType],
    Dataset[DataType],
    Generic[DataType, TransformType],
):
    def __init__(
        self,
        num_domains: int,
        transforms: TransformType | Sequence[TransformType | None] | None = None,
    ) -> None:
        MultiDomain.__init__(self, num_domains, transforms)
        Dataset.__init__(self)

    def __str__(self) -> LiteralString:
        return self.__class__.__name__


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
        transforms: TensorFn | Sequence[TensorFn | None] | None = None,
    ) -> None:
        super().__init__(2, transforms)
