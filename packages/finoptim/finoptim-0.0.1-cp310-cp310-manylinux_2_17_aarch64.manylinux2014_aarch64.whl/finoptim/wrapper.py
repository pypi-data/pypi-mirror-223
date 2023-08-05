import numpy as np
import pandas as pd

# import the contents of the Rust library into the Python extension
# optional: include the documentation from the Rust module

import finoptim.rust_as_backend as rs

from datetime import datetime, date, timedelta

# __all__ = __all__ + ["PythonClass"]

def add_one(x: int) -> int:
    """see if documentation works

    Args:
        x (int): your number

    Returns:
        int: numnber +1
    """
    return x + 1


def cost(usage, prices, savings_plans, reservations)->float:
    """_summary_

    Args:
        usage (_type_): _description_
        prices (_type_): _description_
        savings_plans (_type_): _description_
        reservations (_type_): _description_

    Returns:
        float: the cost associated with the usage, prices and input levels of commitments
    """
    if isinstance(usage, pd.DataFrame):
        assert isinstance(usage.index.dtype, datetime)
        X = usage.values
    levels = np.array(np.append(savings_plans,reservations)).astype(int)
    return rs.cost(usage, prices, levels)


class PythonClass:
    def __init__(self, value: int) -> None:
        self.value = value