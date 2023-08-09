# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = ("GAN",)

from typing import TYPE_CHECKING

import torch
import torch.nn.functional as F
from lightning import LightningModule

if TYPE_CHECKING:
    from torch import Tensor


class GAN(LightningModule):
    def __init__(self) -> None:
        super().__init__()
        self.automatic_optimization = False

    @classmethod
    def get_label(cls, pred: Tensor, as_real: bool = True) -> Tensor:
        return torch.ones_like(pred) if as_real else torch.zeros_like(pred)

    @classmethod
    def adversarial_loss(cls, pred: Tensor, as_real: bool = True) -> Tensor:
        label = cls.get_label(pred, as_real)
        return F.binary_cross_entropy(pred, label)
