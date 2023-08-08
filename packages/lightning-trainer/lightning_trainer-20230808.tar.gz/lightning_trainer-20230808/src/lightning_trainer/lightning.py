import pytorch_lightning as pl
import torch.nn as nn
from torch.utils.data import DataLoader
import torch  # do not remove
from .config import instantiate_from_config
from .logger import Logger


def get_batch_size(batch):
    if isinstance(batch, list):
        batch_size = len(batch)
    elif isinstance(batch, dict):
        batch_size = batch[list(batch.keys())[0]].shape[0]
    else:
        assert False
    return batch_size

class LightningModel(pl.LightningModule):
    def __init__(
        self, model: nn.Module, optimizer_cfg, scheduler_cfg, log_dir: str
    ) -> None:
        super().__init__()

        self.model: nn.Module = model
        self.optimizer_cfg = optimizer_cfg
        self.scheduler_cfg = scheduler_cfg
        self.model._log_dir = log_dir
        self.validation_loss_dict = dict()
        self.validation_samples_num = 0

    def configure_optimizers(self):
        """配置优化器"""

        # optimizer
        optimizer_cls = f"torch.optim.{self.optimizer_cfg.target}"
        Logger.info(f"optimizer:{optimizer_cls}")
        optimizer = eval(optimizer_cls)(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            **self.optimizer_cfg.params,
        )

        # scheduler
        scheduler_cls = f"torch.optim.lr_scheduler.{self.scheduler_cfg.target}"
        Logger.info(f"scheduler:{scheduler_cls}")
        scheduler = eval(scheduler_cls)(optimizer, **self.scheduler_cfg.params)

        return ({"optimizer": optimizer, "lr_scheduler": scheduler},)

    def training_step(self, batch, batch_idx):
        # run_train
        # self.model._epoch = self.current_epoch
        # self.model._train_step += 1

        batch_size = get_batch_size(batch)
        total_loss, loss_dict = self.model.forward_train(batch, batch_idx)

        for name, value in loss_dict.items():
            self.log(
                f"train/{name}",
                value,
                on_step=True,
                on_epoch=False,
                sync_dist=True,
                batch_size=batch_size,
            )

        for name, value in loss_dict.items():
            self.log(
                f"train_epoch/{name}",
                value,
                on_step=False,
                on_epoch=True,
                sync_dist=True,
                batch_size=batch_size,
            )

        return total_loss

    def validation_step(self, batch, batch_idx):
        # self.model._validation_step += 1

        batch_size = get_batch_size(batch)
        self.validation_samples_num += batch_size

        total_loss, loss_dict = self.model.forward_validation(batch, batch_idx)

        for name, value in loss_dict.items():
            self.log(
                f"validation/{name}",
                value,
                on_epoch=True,
                sync_dist=True,
                batch_size=batch_size,
            )

            if name not in self.validation_loss_dict:
                self.validation_loss_dict[name] = 0
            self.validation_loss_dict[name] += value * batch_size

        self.log(
            "validation_loss",
            total_loss,
            prog_bar=True,
            sync_dist=True,
            batch_size=batch_size,
        )

    def on_validation_epoch_end(self):
        text = f"epoch={self.current_epoch:03d}, "
        for name, value in self.validation_loss_dict.items():
            loss = value / self.validation_samples_num
            text += f"{name}={loss:.5f}, "

        Logger.info(text[:-2])

        # clear
        self.validation_samples_num = 0
        self.validation_loss_dict = dict()


def get_dataloader(cfg, mode: str = "train"):
    if not hasattr(cfg, mode + "_dataset"):
        print(f"no {mode}_dataset")
        return None

    if not hasattr(cfg, mode + "_dataloader"):
        print(f"no {mode}_dataloader")
        return None
    
    dataset = instantiate_from_config(getattr(cfg, mode + "_dataset"))
    dataloader_cfg = getattr(cfg, mode + "_dataloader")
    if not hasattr(dataloader_cfg, "type"):
        dataloader = DataLoader(dataset=dataset, **dataloader_cfg)
    else:
        assert False # TODO Self-implemented dataloader
    return dataloader
