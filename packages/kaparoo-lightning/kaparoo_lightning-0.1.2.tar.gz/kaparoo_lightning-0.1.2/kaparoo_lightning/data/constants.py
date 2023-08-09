# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("BATCH_SIZE", "MAX_WORKERS", "NUM_WORKERS", "STAGES", "SUBSETS")

import os
from typing import TYPE_CHECKING, Final

from torch import cuda

if TYPE_CHECKING:
    from typing_extensions import LiteralString

_USE_GPU = cuda.is_available()
BATCH_SIZE_3XS: Final[int] = 4 if _USE_GPU else 1
BATCH_SIZE_2XS: Final[int] = 8 if _USE_GPU else 2
BATCH_SIZE_XS: Final[int] = 16 if _USE_GPU else 4
BATCH_SIZE_S: Final[int] = 32 if _USE_GPU else 8
BATCH_SIZE_M: Final[int] = 64 if _USE_GPU else 16
BATCH_SIZE_L: Final[int] = 128 if _USE_GPU else 32
BATCH_SIZE_XL: Final[int] = 256 if _USE_GPU else 64
BATCH_SIZE_2XL: Final[int] = 512 if _USE_GPU else 128
BATCH_SIZE_3XL: Final[int] = 1024 if _USE_GPU else 256
BATCH_SIZE: Final[int] = BATCH_SIZE_M

_CPU_COUNT = os.cpu_count()
MAX_WORKERS: Final[int] = _CPU_COUNT if isinstance(_CPU_COUNT, int) else 0
NUM_WORKERS: Final[int] = MAX_WORKERS // 2

STAGES: Final[tuple[LiteralString, ...]] = ("fit", "validate", "test", "predict")
SUBSETS: Final[tuple[LiteralString, ...]] = ("train", "valid", "test", "pred")
