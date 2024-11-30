from flask import Blueprint, jsonify

from webapp import api_client

metrics = Blueprint(
    "routes", __name__, static_folder="static", template_folder="templates"
)


@metrics.route("/average")
def rainfall_average():
    return jsonify(
        api_client.get_rainfall_average(
            time_mode="yearly", begin_year=1991, end_year=2021
        )
    )


@metrics.route("/normal")
def rainfall_normal():
    return jsonify(
        api_client.get_rainfall_normal(
            time_mode="monthly", begin_year=1985, month="May"
        )
    )


@metrics.route("/relative_distance_to_normal")
def rainfall_relative_distance_to_normal():
    return jsonify(
        api_client.get_rainfall_relative_distance_to_normal(
            time_mode="seasonal",
            begin_year=1995,
            normal_year=1975,
            season="fall",
        )
    )


@metrics.route("/years_below_normal")
def years_below_normal():
    return jsonify(
        api_client.get_years_below_normal(
            time_mode="yearly",
            normal_year=1981,
            begin_year=2003,
            end_year=2023,
        )
    )


@metrics.route("/years_above_normal")
def years_above_normal():
    return jsonify(
        api_client.get_years_above_normal(
            time_mode="yearly",
            normal_year=1981,
            begin_year=2003,
            end_year=2023,
        )
    )


@metrics.route("/standard_deviation")
def rainfall_standard_deviation():
    return jsonify(
        api_client.get_rainfall_standard_deviation(
            time_mode="seasonal",
            begin_year=2005,
            end_year=2020,
            season="winter",
            weigh_by_average=True,
        )
    )
