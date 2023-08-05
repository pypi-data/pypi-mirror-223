# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("MultiDomainDataset", "DoubleDomainDataset")

from typing import TYPE_CHECKING, Generic

from torch.utils.data import Dataset

from kaparoo_lightning.data.dataset.traits import MultiDomain

if TYPE_CHECKING:
    from collections.abc import Sequence

    from torch import Tensor

    from kaparoo_lightning.common.types import TensorFn
    from kaparoo_lightning.data.dataset.types import DataType, TransformType


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


class MultiDomainDataset(_MultiDomainDataset[tuple[Tensor, ...], TensorFn]):
    pass


class DoubleDomainDataset(_MultiDomainDataset[tuple[Tensor, Tensor], TensorFn]):
    pass
