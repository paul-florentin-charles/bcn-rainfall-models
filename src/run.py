"""
File to run the future application.
For the moment, it merely runs a script to test functionalities.
"""

from src.classes.monthly_rainfall import MonthlyRainfall
from src.classes.seasonal_rainfall import SeasonalRainfall
from src.classes.yearly_rainfall import YearlyRainfall
from src.enums.months import Month
from src.enums.seasons import Season


def run() -> None:
    """
    Temporary function to test use cases.
    Should later launch the application.

    :return: None
    """
    by_year: bool = True
    by_month: bool = False

    month: Month = Month.JULY
    season: Season = Season.SUMMER

    if by_year:
        yearly_rainfall: YearlyRainfall = YearlyRainfall()
    elif by_month:
        yearly_rainfall: MonthlyRainfall = MonthlyRainfall(month)
    else:
        yearly_rainfall: SeasonalRainfall = SeasonalRainfall(season)

    avg_1970_2000 = yearly_rainfall.get_average_yearly_rainfall(1970, 2000)
    avg_1980_2010 = yearly_rainfall.get_average_yearly_rainfall(1980, 2010)
    avg_1990_2020 = yearly_rainfall.get_average_yearly_rainfall(1990, 2020)

    print("Normal 1970 - 2000:", avg_1970_2000)
    print("Normal 1980 - 2010:", avg_1980_2010)
    print("Normal 1990 - 2020:", avg_1990_2020)

    yearly_rainfall.add_percentage_of_normal(1980, 2010)

    print("Number of years above normal:", yearly_rainfall.get_years_above_average())
    print("Number of years below normal", yearly_rainfall.get_years_below_average())

    r2_score, slope = yearly_rainfall.add_linear_regression()
    print("R2 score:", r2_score)
    print("Slope (in mm/year):", slope)

    yearly_rainfall.add_savgol_filter()
    yearly_rainfall.add_kmeans()

    yearly_rainfall.plot_rainfall()
    yearly_rainfall.plot_normal()


if __name__ == "__main__":
    run()
