from numpy import linalg as LA
import torch


def checkNorm(ts):
    if isinstance(ts, torch.Tensor):
        with torch.no_grad():
            res = torch.norm(ts).item();
            return res
    return LA.norm(ts)
