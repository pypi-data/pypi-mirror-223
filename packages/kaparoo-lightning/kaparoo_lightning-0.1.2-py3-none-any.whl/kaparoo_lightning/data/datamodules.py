# -*- coding: utf-8 -*-

from __future__ import annotations

__all__ = (
    "DataModuleBase",
    "DataModule",
    "TransformableDataModule",
    "LabelTransformableDataModule",
)

from typing import TYPE_CHECKING, Generic, TypeVar

from kaparoo.utils.optional import unwrap_or_default
from lightning import LightningDataModule
from torch.utils.data import DataLoader, Dataset

from kaparoo_lightning.common.spec import update_spec
from kaparoo_lightning.data.constants import BATCH_SIZE, NUM_WORKERS, SUBSETS

if TYPE_CHECKING:
    from typing import Any

    from kaparoo.utils.types import T_co
    from typing_extensions import LiteralString

    from kaparoo_lightning.data.dataloaders import DataLoaderSpec


TransformType = TypeVar("TransformType")
LabelTransformType = TypeVar("LabelTransformType")


class DataModuleBase(LightningDataModule, Generic[T_co]):
    def __init__(self) -> None:
        super().__init__()
        self.dataset_train: Dataset[T_co] | None = None
        self.dataset_valid: Dataset[T_co] | None = None
        self.dataset_test: Dataset[T_co] | None = None
        self.dataset_pred: Dataset[T_co] | None = None

    @property
    def has_train(self) -> bool:
        return isinstance(self.dataset_train, Dataset)

    @property
    def has_valid(self) -> bool:
        return isinstance(self.dataset_valid, Dataset)

    @property
    def has_test(self) -> bool:
        return isinstance(self.dataset_test, Dataset)

    @property
    def has_pred(self) -> bool:
        return isinstance(self.dataset_pred, Dataset)

    def __str__(self) -> LiteralString:
        return self.__class__.__name__


class DataModule(DataModuleBase[T_co]):
    def __init__(
        self,
        batch_size: int = BATCH_SIZE,
        num_workers: int = NUM_WORKERS,
        shuffle: bool = True,
        *,
        # `Dataset`
        max_trains: int | None = None,
        max_valids: int | None = None,
        max_tests: int | None = None,
        max_preds: int | None = None,
        # `DataLoader`
        dataloader_spec: DataLoaderSpec | None = None,
        train_loader_spec: DataLoaderSpec | None = None,
        valid_loader_spec: DataLoaderSpec | None = None,
        test_loader_spec: DataLoaderSpec | None = None,
        pred_loader_spec: DataLoaderSpec | None = None,
    ) -> None:
        super().__init__()

        self.use_train = max_trains != 0
        self.use_valid = max_valids != 0
        self.use_test = max_tests != 0
        self.use_pred = max_preds != 0

        if not (self.use_train or self.use_valid or self.use_test or self.use_pred):
            raise ValueError(f"cannot create {self} when none of the datasets exist")

        self.max_trains = max_trains
        self.max_valids = max_valids
        self.max_tests = max_tests
        self.max_preds = max_preds

        default_spec: DataLoaderSpec = unwrap_or_default(dataloader_spec, {})  # type: ignore[assignment] # noqa: E501
        train_spec = unwrap_or_default(train_loader_spec, default_spec)
        valid_spec = unwrap_or_default(valid_loader_spec, default_spec)
        pred_spec = unwrap_or_default(pred_loader_spec, default_spec)
        test_spec = unwrap_or_default(test_loader_spec, default_spec)

        essential_spec: DataLoaderSpec = {
            "batch_size": batch_size,
            "num_workers": num_workers,
            "shuffle": shuffle,
        }

        self.train_loader_spec = update_spec(essential_spec, train_spec)
        self.valid_loader_spec = update_spec(essential_spec, valid_spec)
        self.test_loader_spec = update_spec(essential_spec, test_spec)
        self.pred_loader_spec = update_spec(essential_spec, pred_spec)

    @property
    def config(self) -> dict[str, Any]:
        return {s: self.get_config(s) for s in SUBSETS}

    def get_config(self, subset: str) -> dict[str, Any]:
        if subset not in SUBSETS:
            raise KeyError(f"`subset` must be one of {SUBSETS} (got {subset})")
        return {
            "dataset": {
                "use": getattr(self, f"use_{subset}"),
                "max": getattr(self, f"max_{subset}s"),
            },
            "dataloader": getattr(self, f"{subset}_loader_spec"),
        }

    def train_dataloader(self) -> DataLoader[T_co]:
        if not self.has_train:
            raise AttributeError(f"{self} does not have a dataset for training")
        return DataLoader(self.dataset_train, **self.train_loader_spec)  # type: ignore[arg-type]  # noqa: E501

    def val_dataloader(self) -> DataLoader[T_co]:
        if not self.has_valid:
            raise AttributeError(f"{self} does not have a dataset for validation")
        return DataLoader(self.dataset_valid, **self.valid_loader_spec)  # type: ignore[arg-type]  # noqa: E501

    def test_dataloader(self) -> DataLoader[T_co]:
        if not self.has_test:
            raise AttributeError(f"{self} does not have a dataset for testing")
        return DataLoader(self.dataset_test, **self.test_loader_spec)  # type: ignore[arg-type]  # noqa: E501

    def predict_dataloader(self) -> DataLoader[T_co]:
        if not self.has_pred:
            raise AttributeError(f"{self} does not have a dataset for prediction")
        return DataLoader(self.dataset_pred, **self.pred_loader_spec)  # type: ignore[arg-type]  # noqa: E501


class TransformableDataModule(DataModule[T_co], Generic[T_co, TransformType]):
    def __init__(
        self,
        batch_size: int = BATCH_SIZE,
        num_workers: int = NUM_WORKERS,
        shuffle: bool = True,
        *,
        # `Dataset`
        max_trains: int | None = None,
        max_valids: int | None = None,
        max_tests: int | None = None,
        max_preds: int | None = None,
        # `Dataset` transforms
        transform: TransformType | None = None,
        transform_train: TransformType | None = None,
        transform_valid: TransformType | None = None,
        transform_test: TransformType | None = None,
        transform_pred: TransformType | None = None,
        # `DataLoader`
        dataloader_spec: DataLoaderSpec | None = None,
        train_loader_spec: DataLoaderSpec | None = None,
        valid_loader_spec: DataLoaderSpec | None = None,
        test_loader_spec: DataLoaderSpec | None = None,
        pred_loader_spec: DataLoaderSpec | None = None,
    ) -> None:
        super().__init__(
            batch_size,
            num_workers,
            shuffle,
            max_trains=max_trains,
            max_valids=max_valids,
            max_tests=max_tests,
            max_preds=max_preds,
            dataloader_spec=dataloader_spec,
            train_loader_spec=train_loader_spec,
            valid_loader_spec=valid_loader_spec,
            test_loader_spec=test_loader_spec,
            pred_loader_spec=pred_loader_spec,
        )

        self.transform_train = unwrap_or_default(transform_train, transform)
        self.transform_valid = unwrap_or_default(transform_valid, transform)
        self.transform_test = unwrap_or_default(transform_test, transform)
        self.transform_pred = unwrap_or_default(transform_pred, transform)

    def get_config(self, subset: str) -> dict[str, Any]:
        config = super().get_config(subset)
        config["dataset"]["transform"] = getattr(self, f"transform_{subset}")
        return config


class LabelTransformableDataModule(
    TransformableDataModule[T_co, TransformType],
    Generic[T_co, TransformType, LabelTransformType],
):
    def __init__(
        self,
        batch_size: int = BATCH_SIZE,
        num_workers: int = NUM_WORKERS,
        shuffle: bool = True,
        *,
        # `Dataset`
        max_trains: int | None = None,
        max_valids: int | None = None,
        max_tests: int | None = None,
        max_preds: int | None = None,
        # `Dataset` transforms
        transform: TransformType | None = None,
        transform_train: TransformType | None = None,
        transform_valid: TransformType | None = None,
        transform_test: TransformType | None = None,
        transform_pred: TransformType | None = None,
        # `Dataset` label transforms
        label_transform: LabelTransformType | None = None,
        label_transform_train: LabelTransformType | None = None,
        label_transform_valid: LabelTransformType | None = None,
        label_transform_test: LabelTransformType | None = None,
        label_transform_pred: LabelTransformType | None = None,
        # `DataLoader`
        dataloader_spec: DataLoaderSpec | None = None,
        train_loader_spec: DataLoaderSpec | None = None,
        valid_loader_spec: DataLoaderSpec | None = None,
        test_loader_spec: DataLoaderSpec | None = None,
        pred_loader_spec: DataLoaderSpec | None = None,
    ) -> None:
        super().__init__(
            batch_size,
            num_workers,
            shuffle,
            max_trains=max_trains,
            max_valids=max_valids,
            max_tests=max_tests,
            max_preds=max_preds,
            transform=transform,
            transform_train=transform_train,
            transform_valid=transform_valid,
            transform_test=transform_test,
            transform_pred=transform_pred,
            dataloader_spec=dataloader_spec,
            train_loader_spec=train_loader_spec,
            valid_loader_spec=valid_loader_spec,
            test_loader_spec=test_loader_spec,
            pred_loader_spec=pred_loader_spec,
        )

        default = label_transform
        self.label_transform_train = unwrap_or_default(label_transform_train, default)
        self.label_transform_valid = unwrap_or_default(label_transform_valid, default)
        self.label_transform_test = unwrap_or_default(label_transform_test, default)
        self.label_transform_pred = unwrap_or_default(label_transform_pred, default)

    def get_config(self, subset: str) -> dict[str, Any]:
        config = super().get_config(subset)
        label_transform = getattr(self, f"label_transform_{subset}")
        config["dataset"]["label_transform"] = label_transform
        return config
