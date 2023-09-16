"""
Provides decorators for plotting with Matplotlib.
"""

from typing import Callable, Optional

import matplotlib.pyplot as plt

from src.core.utils.enums.labels import Label


def legend(ylabel: Optional[str] = f"{Label.RAINFALL.value} in (mm)") -> Callable:
    """
    Add labels to x-axis and y-axis and enable legend plot.

    :return: A callable function that takes any number of arguments.
    """

    def decorator(func: Callable):
        def wrapper(*args):
            func(*args)
            plt.xlabel(Label.YEAR.value)
            plt.ylabel(ylabel)
            plt.legend()

        return wrapper

    return decorator
