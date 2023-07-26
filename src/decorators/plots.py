"""
Provides decorators for plotting with Matplotlib.
"""

from typing import Callable, Optional

import matplotlib.pyplot as plt

from src.enums.labels import Label


def legend_and_show(ylabel: Optional[str] = f"{Label.RAINFALL.value} in (mm)"):
    """
    Add labels to x-axis and y-axis, enable legend and show plot.

    :return: A callable function that takes any number of arguments.
    """

    def decorator(func: Callable):
        def wrapper(*args):
            func(*args)
            plt.xlabel(Label.YEAR.value)
            plt.ylabel(ylabel)
            plt.legend()
            plt.show()

        return wrapper

    return decorator
