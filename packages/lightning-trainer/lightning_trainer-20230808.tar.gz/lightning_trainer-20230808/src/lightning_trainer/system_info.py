import platform
import re
import os

import psutil
import torch
import pytorch_lightning

__all__ = ["get_cpu_info", "get_gpu_info", "get_package_info", "get_memory_info"]


def get_cpu_info() -> dict:
    """cpu info

    Returns:
        dict: keys: ["system", "cpu_name", "cpu_count", "cpu_threads", "cpu_core"]
    """
    UNIX: bool = os.name == "posix"
    if UNIX:
        return {
            "system": platform.version(),
            "cpu_name": re.search(
                "model\s+name\s+:\s+(.+)", read_file("/proc/cpuinfo"), re.I
            ).groups()[0],
            "cpu_count": len(
                set(re.findall("physical id.+", read_file("/proc/cpuinfo")))
            ),
            "cpu_threads": get_cpu_threads(),
            "cpu_core": get_cpu_core(),
        }
    else:
        import wmi  # pip install wmi

        WMI = wmi.WMI()
        cpu_list: list = WMI.Win32_Processor()
        return {
            "system": "Windows" + platform.version(),
            "cpu_name": cpu_list[0].Name,
            "cpu_count": len(cpu_list),
            "cpu_threads": get_cpu_threads(),
            "cpu_core": get_cpu_core(),
        }


def get_gpu_info():
    """gpu info

    Returns:
        dict: keys: ["gpu_name", "gpu_num"]
    """
    return {
        "gpu_name": torch.cuda.get_device_name(0),
        "gpu_num": torch.cuda.device_count(),
    }


def get_memory_info():
    """GB"""
    pc_mem = psutil.virtual_memory()
    gb_factor = 1024.0**3
    return {
        "total": float(pc_mem.total / gb_factor),
        "available": float(pc_mem.available / gb_factor),
        "used": float(pc_mem.used / gb_factor),
    }


def get_package_info():
    """package info

    Returns:
        dict: keys: ["python", "pytorch", "pytorch_lightning", "cuda", "cudnn"]
    """
    return {
        "python": platform.python_version(),
        "pytorch": torch.__version__,
        "pytorch_lightning": pytorch_lightning.__version__,
        "cuda": torch.version.cuda,
        "cudnn": torch.backends.cudnn.version(),
    }


def get_cpu_threads() -> int:
    return psutil.cpu_count()


def get_cpu_core() -> int:
    return psutil.cpu_count(logical=False)


def read_file(filename) -> str:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except:
        pass

    return ""
