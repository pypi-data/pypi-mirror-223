# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("DataLoaderSpec",)

from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING

from kaparoo_lightning.common.spec import SpecBase

if TYPE_CHECKING:
    from typing import Any

    from torch.utils.data import Sampler
    from torch.utils.data.dataloader import _collate_fn_t, _worker_init_fn_t


class DataLoaderSpec(SpecBase, total=False):
    batch_size: int | None
    shuffle: bool | None
    sampler: Sampler | Iterable | None
    batch_sampler: Sampler[Sequence] | Iterable[Sequence] | None
    num_workers: int
    collate_fn: _collate_fn_t | None
    pin_memory: bool
    drop_last: bool
    timeout: float
    worker_init_fn: _worker_init_fn_t | None
    multiprocessing_context: Any | None
    generator: Any | None
    prefetch_factor: int | None
    persistent_workers: bool
    pin_memory_device: str
