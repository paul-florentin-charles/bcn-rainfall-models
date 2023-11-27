import matplotlib.pyplot as plt
import numpy.random as nprand

from src.core.utils.decorators import plots


@plots.legend()
def test_legend():
    plt.scatter(nprand.randint(1950, 2020, size=100), nprand.randint(0, 1000, size=100))
