from flask import Blueprint, jsonify, render_template

from webapp import api_client, BEGIN_YEAR, END_YEAR, NORMAL_YEAR

metrics = Blueprint(
    "metrics", __name__, static_folder="static", template_folder="templates"
)


@metrics.route("/rainfall_average")
def rainfall_average():
    return render_template(
        "sections/rainfall_average.html",
        plotlyRainfallAverageJSON=api_client.get_rainfall_by_year_as_plotly_json(
            time_mode="yearly",
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            plot_average=True,
            plot_linear_regression=True,
        ),
    )


@metrics.route("/rainfall_normal")
def rainfall_normal():
    return jsonify(
        api_client.get_rainfall_normal(
            time_mode="monthly", begin_year=BEGIN_YEAR, month="May"
        )
    )


@metrics.route("/relative_distance_to_normal")
def rainfall_relative_distance_to_normal():
    return jsonify(
        api_client.get_rainfall_relative_distance_to_normal(
            time_mode="seasonal",
            begin_year=BEGIN_YEAR,
            normal_year=NORMAL_YEAR,
            end_year=END_YEAR,
            season="fall",
        )
    )


@metrics.route("/years_below_normal")
def years_below_normal():
    return jsonify(
        api_client.get_years_below_normal(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
    )


@metrics.route("/years_above_normal")
def years_above_normal():
    return jsonify(
        api_client.get_years_above_normal(
            time_mode="yearly",
            normal_year=NORMAL_YEAR,
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
        )
    )


@metrics.route("/rainfall_standard_deviation")
def rainfall_standard_deviation():
    return jsonify(
        api_client.get_rainfall_standard_deviation(
            time_mode="seasonal",
            begin_year=BEGIN_YEAR,
            end_year=END_YEAR,
            season="winter",
            weigh_by_average=True,
        )
    )
