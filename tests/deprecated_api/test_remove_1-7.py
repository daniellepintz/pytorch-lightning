# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Test deprecated functionality which will be removed in v1.7.0 """
from unittest import mock

import pytest

from pytorch_lightning import LightningDataModule, Trainer
from pytorch_lightning.loggers import TestTubeLogger
from tests.deprecated_api import _soft_unimport_module
from tests.helpers import BoringModel
from tests.helpers.datamodules import MNISTDataModule
from pytorch_lightning import Callback
from pytorch_lightning.utilities.warnings import rank_zero_deprecation, rank_zero_warn
from pytorch_lightning.utilities.exceptions import MisconfigurationException
from pytorch_lightning.utilities.model_helpers import is_overridden


def test_v1_7_0_deprecated_lightning_module_summarize(tmpdir):
    from pytorch_lightning.core.lightning import warning_cache

    model = BoringModel()
    model.summarize(max_depth=1)
    assert any("The `LightningModule.summarize` method is deprecated in v1.5" in w for w in warning_cache)
    warning_cache.clear()


def test_v1_7_0_moved_model_summary_and_layer_summary(tmpdir):
    _soft_unimport_module("pytorch_lightning.core.memory")
    with pytest.deprecated_call(match="to `pytorch_lightning.utilities.model_summary` since v1.5"):
        from pytorch_lightning.core.memory import LayerSummary, ModelSummary  # noqa: F401


def test_v1_7_0_moved_get_memory_profile_and_get_gpu_memory_map(tmpdir):
    _soft_unimport_module("pytorch_lightning.core.memory")
    with pytest.deprecated_call(match="to `pytorch_lightning.utilities.memory` since v1.5"):
        from pytorch_lightning.core.memory import get_gpu_memory_map, get_memory_profile  # noqa: F401


def test_v1_7_0_deprecated_model_size():
    model = BoringModel()
    with pytest.deprecated_call(
        match="LightningModule.model_size` property was deprecated in v1.5 and will be removed in v1.7"
    ):
        _ = model.model_size


def test_v1_7_0_datamodule_transform_properties(tmpdir):
    dm = MNISTDataModule()
    with pytest.deprecated_call(match=r"DataModule property `train_transforms` was deprecated in v1.5"):
        dm.train_transforms = "a"
    with pytest.deprecated_call(match=r"DataModule property `val_transforms` was deprecated in v1.5"):
        dm.val_transforms = "b"
    with pytest.deprecated_call(match=r"DataModule property `test_transforms` was deprecated in v1.5"):
        dm.test_transforms = "c"
    with pytest.deprecated_call(match=r"DataModule property `train_transforms` was deprecated in v1.5"):
        _ = LightningDataModule(train_transforms="a")
    with pytest.deprecated_call(match=r"DataModule property `val_transforms` was deprecated in v1.5"):
        _ = LightningDataModule(val_transforms="b")
    with pytest.deprecated_call(match=r"DataModule property `test_transforms` was deprecated in v1.5"):
        _ = LightningDataModule(test_transforms="c")
    with pytest.deprecated_call(match=r"DataModule property `test_transforms` was deprecated in v1.5"):
        _ = LightningDataModule(test_transforms="c", dims=(1, 1, 1))


def test_v1_7_0_datamodule_size_property(tmpdir):
    dm = MNISTDataModule()
    with pytest.deprecated_call(match=r"DataModule property `size` was deprecated in v1.5"):
        dm.size()


def test_v1_7_0_datamodule_dims_property(tmpdir):
    dm = MNISTDataModule()
    with pytest.deprecated_call(match=r"DataModule property `dims` was deprecated in v1.5"):
        _ = dm.dims
    with pytest.deprecated_call(match=r"DataModule property `dims` was deprecated in v1.5"):
        _ = LightningDataModule(dims=(1, 1, 1))


def test_v1_7_0_trainer_prepare_data_per_node(tmpdir):
    with pytest.deprecated_call(
        match="Setting `prepare_data_per_node` with the trainer flag is deprecated and will be removed in v1.7.0!"
    ):
        _ = Trainer(prepare_data_per_node=False)


def test_v1_7_0_deprecated_on_train_dataloader(tmpdir):

    model = BoringModel()
    with pytest.deprecated_call(
        match="Method `on_train_dataloader` in DataHooks is deprecated and will be removed in v1.7.0."
    ):
        model.on_train_dataloader()
    with pytest.deprecated_call(
        match="Method `on_val_dataloader` in DataHooks is deprecated and will be removed in v1.7.0."
    ):
        model.on_val_dataloader()
    with pytest.deprecated_call(
        match="Method `on_test_dataloader` in DataHooks is deprecated and will be removed in v1.7.0."
    ):
        model.on_test_dataloader()
    with pytest.deprecated_call(
        match="Method `on_predict_dataloader` in DataHooks is deprecated and will be removed in v1.7.0."
    ):
        model.on_predict_dataloader()


@mock.patch("pytorch_lightning.loggers.test_tube.Experiment")
def test_v1_7_0_test_tube_logger(_, tmpdir):
    with pytest.deprecated_call(match="The TestTubeLogger is deprecated since v1.5 and will be removed in v1.7"):
        _ = TestTubeLogger(tmpdir)


def test_v1_7_0_on_interrupt(tmpdir):
    class HandleInterruptCallback(Callback):
        def on_keyboard_interrupt(self, trainer, pl_module):
            self.log("keyboard interrupt")

    model = BoringModel()
    handle_interrupt_callback = HandleInterruptCallback()

    trainer = Trainer(
        callbacks=[handle_interrupt_callback],
        max_epochs=1,
        limit_val_batches=0.1,
        limit_train_batches=0.2,
        progress_bar_refresh_rate=0,
        logger=False,
        default_root_dir=tmpdir,
    )
    if is_overridden(
        method_name="on_keyboard_interrupt", instance=handle_interrupt_callback, parent=HandleInterruptCallback
    ):
        rank_zero_deprecation("FINDME FINDME FINDME FINDME")

    with pytest.deprecated_call(
        match="The `on_keyboard_interrupt` callback hook was deprecated in v1.5 and will be removed in v1.7"
    ):
        trainer.fit(model)
