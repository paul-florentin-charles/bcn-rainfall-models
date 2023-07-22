from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from src.classes.monthly_rainfall import MonthlyRainfall
from src.classes.seasonal_rainfall import SeasonalRainfall
from src.classes.yearly_rainfall import YearlyRainfall
from src.enums.months import Month
from src.enums.seasons import Season

year_step = 10


def build_and_fit_mlp_to_predict_years_below_normal_for_decade(yearly_rainfall_obj: YearlyRainfall) -> \
        tuple[MLPClassifier, StandardScaler]:
    # Building training data
    X = []
    y = []
    for year in range(yearly_rainfall_obj.get_yearly_rainfall()["Year"].iloc[0],
                      yearly_rainfall_obj.get_yearly_rainfall()["Year"].iloc[-1] // year_step * year_step,
                      year_step):
        years = []
        for year2 in range(year, year + year_step):
            years.append(year2)
        X.append(years)
        tmp_yearly_rainfall_obj = YearlyRainfall(yearly_rainfall=yearly_rainfall_obj.get_yearly_rainfall())
        y.append(tmp_yearly_rainfall_obj.get_years_below_average(year, year + year_step - 1))

    # Preprocessing data
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    # Building and training model
    clf = MLPClassifier(solver='lbfgs',
                        alpha=1e-5,
                        hidden_layer_sizes=(5, year_step),
                        random_state=1,
                        max_iter=1000)
    clf.fit(X, y)

    return clf, scaler


def run():
    by_year: bool = False
    by_month: bool = False

    if by_year:
        yearly_rainfall: YearlyRainfall = YearlyRainfall()
    elif by_month:
        yearly_rainfall: MonthlyRainfall = MonthlyRainfall(Month.JANUARY)
    else:
        yearly_rainfall: SeasonalRainfall = SeasonalRainfall(Season.WINTER)

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
    print("Slope (in mm/year)", slope)

    yearly_rainfall.add_savgol_filter()

    yearly_rainfall.plot_rainfall()
    yearly_rainfall.plot_normal()


if __name__ == "__main__":
    run()
