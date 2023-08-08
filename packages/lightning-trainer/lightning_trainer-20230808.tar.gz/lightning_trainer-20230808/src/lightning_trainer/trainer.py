import argparse
import os
import os.path as osp
import sys

import pytorch_lightning as pl
import torch
import torch.nn as nn
from lightning import seed_everything
from omegaconf import OmegaConf
from pytorch_lightning.callbacks import LearningRateMonitor, ModelCheckpoint
from pytorch_lightning.trainer import Trainer

from .config import get_log_dir, instantiate_from_config, save_json
from .lightning import LightningModel, get_dataloader
from .logger import Logger
from .parameters import export_model_parameters
from .system_info import get_cpu_info, get_gpu_info, get_package_info


def train(config_filename: str):
    assert osp.exists(config_filename), "Config file is not exist!"

    config = OmegaConf.load(osp.abspath(config_filename))
    exp_folder = get_log_dir(config_filename)

    log_filename = osp.join(exp_folder, "train.log")
    if osp.exists(log_filename):
        Logger.warn("训练日志文件存在,删除日志文件并重新训练")
    Logger.logfile(log_filename, clear=True)

    # export conda environments
    environments_filename = osp.join(exp_folder, "environments.yaml")
    os.system(f"conda env export > {environments_filename}")
    Logger.info(f"save: {environments_filename}")

    # save config
    fn = osp.join(exp_folder, "config.yaml")
    OmegaConf.save(config, fn)
    Logger.info(f"save: {fn}")

    # hardware info
    hardware_info = {}
    hardware_info.update(get_gpu_info())
    hardware_info.update(get_cpu_info())
    hardware_info.update(get_package_info())
    save_json(osp.join(exp_folder, "hardware.json"), hardware_info)

    # seed
    seed_everything(config.base.seed)

    Logger.info("prepare to build model...")
    model = instantiate_from_config(config.model)

    # Save Model Parameter Quantities Report
    json_fn = osp.join(exp_folder, "parameters.json")
    save_json(json_fn, export_model_parameters(model))
    Logger.info(f"save: {json_fn}")

    lightning_model = LightningModel(
        model=model,
        optimizer_cfg=config.optimizer,
        scheduler_cfg=config.scheduler,
        log_dir=exp_folder,
    )

    pretrained = config.base.pretrained
    if pretrained:
        state_dict = torch.load(pretrained)["state_dict"]
        lightning_model.load_state_dict(state_dict, strict=True)
        Logger.warn(f"pretrained from:{pretrained}")

    ckpt_path = config.base.ckpt_path
    if ckpt_path:
        Logger.warn(f"resume from:{ckpt_path}")

    if config.base.compile:
        Logger.info("use torch.compile")
        lightning_model = torch.compile(lightning_model)

    Logger.info("prepare to train...")
    trainer = Trainer(
        logger=[
            pl.loggers.TensorBoardLogger(
                save_dir=osp.dirname(osp.dirname(exp_folder)),
                name=exp_folder.split(osp.sep)[-2],
                version=exp_folder.split(osp.sep)[-1],
            ),
        ],
        callbacks=[
            LearningRateMonitor(logging_interval="step"),
            ModelCheckpoint(
                dirpath=osp.join(exp_folder, "checkpoint"),
                monitor="validation_loss",
                filename="{epoch:03d}_{validation_loss:.6f}",
                **config.checkpoint,
            ),
        ],
        **config.trainer,
    )
    trainer.fit(
        lightning_model,
        get_dataloader(config, "train"),
        get_dataloader(config, "validation"),
        ckpt_path=ckpt_path,
    )


def run_train():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "config", default="config.yaml", type=str, help="config filename"
    )
    args = parser.parse_args()
    if not osp.exists(args.config):
        Logger.error(f"not exists: {args.config}")
        sys.exit(0)
    train(args.config)


if __name__ == "__main__":
    run_train()
