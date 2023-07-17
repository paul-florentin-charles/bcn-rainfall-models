import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from sklearn import linear_model, metrics, neural_network, preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from classes.yearly_rainfall import YearlyRainfall

dataset_url = str.format("https://opendata-ajuntament.barcelona.cat/data/dataset/{0}/resource/{1}/download/{2}",
                         "5334c15e-0d70-410b-85f3-d97740ffc1ed",
                         "6f1fb778-0767-478b-b332-c64a833d26d2",
                         "precipitacionsbarcelonadesde1786.csv")

starting_year = 1970
year_step = 10


def apply_linear_regression_to_yearly_rainfall(yearly_rainfall: pd.DataFrame) -> pd.DataFrame:
    reg = linear_model.LinearRegression()
    reg.fit(yearly_rainfall["Year"].values.reshape(-1, 1), yearly_rainfall["Rainfall"].values)
    yearly_rainfall["Linear Regression"] = reg.predict(yearly_rainfall["Year"].values.reshape(-1, 1))

    print("Coefficient of determination:", metrics.r2_score(yearly_rainfall["Rainfall"].values,
                                                            yearly_rainfall["Linear Regression"].values))
    print("Slope (mm/year):", reg.coef_[0])

    return yearly_rainfall


def apply_savgol_filter_to_yearly_rainfall(yearly_rainfall: pd.DataFrame) -> pd.DataFrame:
    yearly_rainfall["Savgol Filter"] = signal.savgol_filter(yearly_rainfall["Rainfall"].values,
                                                            window_length=len(yearly_rainfall["Rainfall"].values),
                                                            polyorder=len(yearly_rainfall) // year_step)

    return yearly_rainfall


def add_deviation_from_normal(yearly_rainfall: pd.DataFrame, normal: float):
    yearly_rainfall['Percentage of normal'] = round(yearly_rainfall['Rainfall'] / normal * 100.0, 2)


def count_years_above_normal(yearly_rainfall: pd.DataFrame) -> int:
    return yearly_rainfall[yearly_rainfall["Percentage of normal"] > 100.0].count()["Year"]


def count_years_below_normal(yearly_rainfall: pd.DataFrame) -> int:
    return yearly_rainfall[yearly_rainfall["Percentage of normal"] < 100.0].count()["Year"]


def build_and_fit_mlp_to_predict_years_below_normal_for_decade(yearly_rainfall: pd.DataFrame,
                                                               normal: float) -> tuple[MLPClassifier, StandardScaler]:
    # Building training data
    X = []
    y = []
    for year in range(yearly_rainfall["Year"].iloc[0], yearly_rainfall["Year"].iloc[-1] // year_step * year_step,
                      year_step):
        years = []
        for year2 in range(year, year + year_step):
            years.append(year2)
        X.append(years)
        tmp_yearly_rainfall = yearly_rainfall[yearly_rainfall["Year"] >= year]
        tmp_yearly_rainfall = tmp_yearly_rainfall[tmp_yearly_rainfall["Year"] < year + year_step]
        y.append(count_years_below_normal(tmp_yearly_rainfall))

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


def plot_yearly_rainfall(yearly_rainfall: pd.DataFrame):
    yearly_rainfall.plot(x="Year",
                         y="Rainfall",
                         ylabel="Rainfall (mm)")


def plot_yearly_rainfall_savgol_filter(yearly_rainfall: pd.DataFrame):
    yearly_rainfall.plot(x="Year",
                         y="Savgol Filter",
                         ylabel="Rainfall (mm)")


def plot_yearly_rainfall_deviation_from_normal(yearly_rainfall: pd.DataFrame):
    yearly_rainfall.plot(x="Year",
                         y="Percentage of normal",
                         label="Percentage of normal (%)",
                         kind="scatter",
                         title="Barcelona rainfall deviation from normal")


def plot_yearly_rainfall_linear_regression(yearly_rainfall: pd.DataFrame):
    yearly_rainfall.plot(x="Year",
                         y="Linear Regression",
                         ylabel="Rainfall (mm)",
                         label="Linear Regression of Rainfall",
                         title="Barcelona linear regression of rainfall")
    plt.scatter(yearly_rainfall["Year"].values.reshape(-1, 1),
                yearly_rainfall["Rainfall"].values,
                color="red",
                label="Rainfall")
    plt.legend()


def run():
    yearly_rainfall_obj = YearlyRainfall()

    avg_1970_2000 = yearly_rainfall_obj.get_average_yearly_rainfall(1970, 2000)
    avg_1980_2010 = yearly_rainfall_obj.get_average_yearly_rainfall(1980, 2010)
    avg_1990_2020 = yearly_rainfall_obj.get_average_yearly_rainfall(1990, 2020)

    print("Normal 1970 - 2000:", avg_1970_2000)
    print("Normal 1980 - 2010:", avg_1980_2010)
    print("Normal 1990 - 2020:", avg_1990_2020)

    add_deviation_from_normal(yearly_rainfall_obj.yearly_rainfall, avg_1980_2010)

    model, scaler = build_and_fit_mlp_to_predict_years_below_normal_for_decade(yearly_rainfall_obj.yearly_rainfall, avg_1980_2010)
    X_predict = [list(range(1960, 1960 + year_step)),
                 list(range(2020, 2020 + year_step)),
                 list(range(2030, 2030 + year_step)),
                 list(range(2080, 2080 + year_step))]
    y = model.predict(scaler.transform(X_predict))
    for idx, x in enumerate(X_predict):
        print(y[idx], "years below normal predicted for these years:", x)

    nb_years_above_normal = count_years_above_normal(yearly_rainfall_obj.yearly_rainfall)
    nb_years_below_normal = count_years_below_normal(yearly_rainfall_obj.yearly_rainfall)
    print("Number of years above normal:", nb_years_above_normal)
    print("Number of years below normal", nb_years_below_normal)

    plot = False
    if plot:
        apply_linear_regression_to_yearly_rainfall(yearly_rainfall_obj.yearly_rainfall)
        plot_yearly_rainfall_linear_regression(yearly_rainfall_obj.yearly_rainfall)

        apply_savgol_filter_to_yearly_rainfall(yearly_rainfall_obj.yearly_rainfall)
        plot_yearly_rainfall_savgol_filter(yearly_rainfall_obj.yearly_rainfall)

        plot_yearly_rainfall_deviation_from_normal(yearly_rainfall_obj.yearly_rainfall)
        plt.axhline(y=100.0, color='orange', linestyle="--", label="Normal")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    run()
