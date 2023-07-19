import matplotlib.pyplot as plt
import pandas as pd
from sklearn import neural_network, preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from classes.yearly_rainfall import YearlyRainfall

starting_year = 1970
year_step = 10


def build_and_fit_mlp_to_predict_years_below_normal_for_decade(yearly_rainfall_obj: YearlyRainfall) -> tuple[
    MLPClassifier, StandardScaler]:
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
        tmp_yearly_rainfall_obj.restrict_to_yearly_interval(year, year + year_step - 1)
        y.append(tmp_yearly_rainfall_obj.get_years_below_average(year, year + year_step - 1))

    # Preprocessing data
    scaler = preprocessing.StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    # Building and training model
    clf = neural_network.MLPClassifier(solver='lbfgs',
                                       alpha=1e-5,
                                       hidden_layer_sizes=(5, year_step),
                                       random_state=1,
                                       max_iter=1000)
    clf.fit(X, y)

    return clf, scaler


def group_yearly_rainfall_by_decade(yearly_rainfall: pd.DataFrame) -> pd.DataFrame:
    decades_rainfall = []
    for year in range(starting_year, yearly_rainfall['Year'].iloc[-1] + 1, 10):
        decade = yearly_rainfall.iloc[year - starting_year: year - starting_year + 10]
        decade.loc[decade["Year"] // 10 == year // 10, "Year"] = year // 10
        decades_rainfall.append(decade.groupby('Year').sum().drop('index', axis='columns'))

    df = decades_rainfall[0]
    for decade_rainfall in decades_rainfall[1:]:
        df = pd.concat((df, decade_rainfall), axis='rows')

    df.index.names = ['Decade']

    return df


def run():
    yearly_rainfall_obj = YearlyRainfall(starting_year=starting_year)

    avg_1970_2000 = yearly_rainfall_obj.get_average_yearly_rainfall(1970, 2000)
    avg_1980_2010 = yearly_rainfall_obj.get_average_yearly_rainfall(1980, 2010)
    avg_1990_2020 = yearly_rainfall_obj.get_average_yearly_rainfall(1990, 2020)

    print("Normal 1970 - 2000:", avg_1970_2000)
    print("Normal 1980 - 2010:", avg_1980_2010)
    print("Normal 1990 - 2020:", avg_1990_2020)

    yearly_rainfall_obj.add_percentage_of_normal(1980, 2010)

    model, scaler = build_and_fit_mlp_to_predict_years_below_normal_for_decade(yearly_rainfall_obj)
    X_predict = [list(range(1960, 1960 + year_step)),
                 list(range(2020, 2020 + year_step)),
                 list(range(2030, 2030 + year_step)),
                 list(range(2080, 2080 + year_step))]
    y = model.predict(scaler.transform(X_predict))
    for idx, x in enumerate(X_predict):
        print(y[idx], "years below normal predicted for these years:", x)

    nb_years_above_normal = yearly_rainfall_obj.get_years_above_average()
    nb_years_below_normal = yearly_rainfall_obj.get_years_below_average()
    print("Number of years above normal:", nb_years_above_normal)
    print("Number of years below normal", nb_years_below_normal)

    yearly_rainfall_obj.add_linear_regression()
    yearly_rainfall_obj.add_savgol_filter()

    print(yearly_rainfall_obj.export_as_csv())

    yearly_rainfall_obj.plot_and_legend_rainfall()
    plt.show()

    yearly_rainfall_obj.plot_and_legend_normal()
    plt.show()


if __name__ == "__main__":
    run()
