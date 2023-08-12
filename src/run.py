"""
File to run the future application.
For the moment, it merely runs a script to test functionalities.
"""
import matplotlib.pyplot as plt

from src.classes.yearly_rainfall import YearlyRainfall
from src.config import Config, CONFIG_FNAME


def run(config: Config) -> None:
    """
    Temporary function to test use cases.
    Should later launch the application.

    :return: None
    """
    yearly_rainfall: YearlyRainfall = YearlyRainfall(config.get_dataset_url(), start_year=1970)

    yearly_rainfall.add_percentage_of_normal(1980, 2010)
    yearly_rainfall.add_linear_regression()
    yearly_rainfall.add_savgol_filter()
    yearly_rainfall.add_kmeans()

    yearly_rainfall.plot_rainfall()
    yearly_rainfall.plot_linear_regression()
    yearly_rainfall.plot_savgol_filter()
    plt.figure()
    yearly_rainfall.plot_normal(True)
    plt.show()


if __name__ == "__main__":
    run(Config(CONFIG_FNAME))
