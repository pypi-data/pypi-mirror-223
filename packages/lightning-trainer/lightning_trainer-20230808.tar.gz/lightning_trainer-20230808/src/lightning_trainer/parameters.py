import torch.nn as nn


def get_parameters_num(model) -> dict:
    total_num = sum(p.numel() for p in model.parameters())
    trainable_num = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"Total": total_num, "Trainable": trainable_num}


def export_model_parameters(model: nn.Module) -> dict:
    """模型参数量报告"""
    parameters_dict = dict()
    for name in dir(model):
        try:
            d = get_parameters_num(getattr(model, name))
            if d["Total"] > 0:
                parameters_dict[name] = d
        except Exception as e:
            pass
    parameters_dict["[ALL]"] = get_parameters_num(model)
    for name in parameters_dict:
        rate = (
            parameters_dict[name]["Trainable"]
            / parameters_dict["[ALL]"]["Trainable"]
            * 100.0
        )
        parameters_dict[name]["Rate(Trainable)"] = f"{rate:.2f}%"
    # TODO 打印表格
    return parameters_dict
