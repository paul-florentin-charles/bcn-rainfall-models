# pylint: disable=missing-docstring

import matplotlib.pyplot as plt
import numpy.random as nprand

from src.decorators import plots


@plots.legend_and_show()
def test_legend_and_show():
    plt.scatter(nprand.random_integers(0, 100, size=100),
                nprand.random_integers(0, 100, size=100))
