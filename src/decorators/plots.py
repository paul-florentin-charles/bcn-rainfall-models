"""
Provides decorators for plotting with Matplotlib.
"""

from typing import Callable

import matplotlib.pyplot as plt

from src.enums.labels import Label


def legend_and_show():
    """
    Add labels to x-axis and y-axis, enable legend and show plot.

    :return: A callable function that takes any number of arguments.
    """

    def decorator(func: Callable):
        def wrapper(*args):
            func(*args)
            plt.xlabel(Label.YEAR.value)
            plt.ylabel(f"{Label.RAINFALL.value} in (mm)")
            plt.legend()
            plt.show()

        return wrapper

    return decorator
