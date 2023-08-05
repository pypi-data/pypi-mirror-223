from numpy import linalg as LA


def checkNorm(ts):
    return LA.norm(ts.cpu().detach().numpy())
