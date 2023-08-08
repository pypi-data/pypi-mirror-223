import importlib
import json
import os


def save_json(filename: str, data, indent: int = 4):
    with open(filename, "w", encoding="utf-8") as fw:
        json.dump(data, fw, ensure_ascii=False, indent=indent)


def get_obj_from_str(string: str, reload: bool = False) -> object:
    """从字符串获取实例

    Args:
        string (str): 实例字符串 (xxx.xxx.xxx)
        reload (bool, optional): Defaults to False.

    Returns:
        object: 实例
    """
    module, cls = string.rsplit(".", 1)
    if reload:
        module_imp = importlib.import_module(module)
        importlib.reload(module_imp)
    return getattr(importlib.import_module(module, package=None), cls)


def instantiate_from_config(config: dict):
    """从配置获取实例

    Args:
        config (dict): config

    Raises:
        KeyError: 必须包含target

    Returns:
        _type_: 实例
    """
    # print(dir(config))
    # if not "target" in config:
    #     raise KeyError("Expected key `target` to instantiate.")

    params = dict()
    for attr in dir(config):
        if attr != "type":
            params[attr] = getattr(config, attr)
    # if "params" in config:
    #     return get_obj_from_str(config["target"])(**config.get("params", dict()))
    # else:
    return get_obj_from_str(config["type"])(**params)


def get_log_dir(config_filename: str):
    """获取log目录"""
    return config_filename.replace("configs" + os.sep, "logs" + os.sep).replace(
        ".yaml", ""
    )
