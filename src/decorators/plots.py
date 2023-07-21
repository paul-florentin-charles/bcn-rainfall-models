import matplotlib.pyplot as plt

from typing import Callable

from src.enums.labels import Label


def legend():
    def decorator(func: Callable):
        def wrapper(*args):
            func(*args)
            plt.xlabel(Label.YEAR.value)
            plt.ylabel(f"{Label.RAINFALL.value} in (mm)")
            plt.legend()
            plt.show()

        return wrapper

    return decorator
