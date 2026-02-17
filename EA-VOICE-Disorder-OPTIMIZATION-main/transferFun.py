# -*- coding: utf-8 -*-
"""
Transfer Functions for Binary Optimization
Compatible with legacy PSO / WOA implementations
"""

import math

# ===================== S-SHAPED TRANSFER FUNCTIONS =====================

def S1(x):
    return 1.0 / (1.0 + math.exp(-2 * x))

def S2(x):
    return 1.0 / (1.0 + math.exp(-x))

def S3(x):
    return 1.0 / (1.0 + math.exp(-x / 2))

def S4(x):
    return 1.0 / (1.0 + math.exp(-x / 3))


# ===================== V-SHAPED TRANSFER FUNCTIONS =====================

def V1(x):
    return abs(math.erf((math.sqrt(math.pi) / 2) * x))

def V2(x):
    return abs(math.tanh(x))

def V3(x):
    return abs(x / math.sqrt(1 + x * x))

def V4(x):
    return abs((2 / math.pi) * math.atan((math.pi / 2) * x))


# ===================== SIGMOID (LEGACY SUPPORT) =====================

def sigmoid_transfer(x):
    """Classic sigmoid transfer function."""
    x = float(x)
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    else:
        z = math.exp(x)
        return z / (1.0 + z)


# ===================== MAIN COMPATIBILITY WRAPPER =====================

def transferFun(x, v=None, fid=2):
    """
    Wrapper expected by PSO.py:
        transferFun(x, v, fid)

    Parameters:
    - x   : position value
    - v   : velocity (ignored, kept for compatibility)
    - fid : transfer function ID

    Returns:
    - probability in [0,1]
    """

    x = float(x)

    # S-shaped functions
    if fid == 1:
        return S1(x)
    elif fid == 2:
        return S2(x)
    elif fid == 3:
        return S3(x)
    elif fid == 4:
        return S4(x)

    # V-shaped functions
    elif fid == 5:
        return V1(x)
    elif fid == 6:
        return V2(x)
    elif fid == 7:
        return V3(x)
    elif fid == 8:
        return V4(x)

    # fallback
    return sigmoid_transfer(x)


# ===================== FACTORY (OPTIONAL) =====================

def get_transfer_function(name="S2"):
    """
    Optional helper to retrieve a transfer function by name.
    """
    name = name.upper()
    if name == "S1":
        return S1
    if name == "S2":
        return S2
    if name == "S3":
        return S3
    if name == "S4":
        return S4
    if name == "V1":
        return V1
    if name == "V2":
        return V2
    if name == "V3":
        return V3
    if name == "V4":
        return V4
    return sigmoid_transfer
