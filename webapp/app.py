"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

import plotly.graph_objs as go
from flask import Flask, render_template
from plotly.io import from_json

from webapp import api_client
from webapp.views import metrics

flask_app = Flask(__name__)
flask_app.register_blueprint(metrics)


def _aggregate_json_traces_as_figure(traces_json: list[str]) -> go.Figure:
    figure = go.Figure()
    for trace_json in traces_json:
        figure.add_traces(list(from_json(trace_json).select_traces()))

    return figure


@flask_app.route("/")
def index():
    begin_year = 1991
    end_year = 2020

    data = api_client.get_rainfall_by_year_as_plotly_json(
        time_mode="seasonal",
        begin_year=begin_year,
        end_year=end_year,
        season="spring",
        plot_average=True,
    )

    monthly_averages = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="monthly",
        begin_year=begin_year,
        end_year=end_year,
    )

    seasonal_averages = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="seasonal",
        begin_year=begin_year,
        end_year=end_year,
    )

    fig_averages = _aggregate_json_traces_as_figure(
        [monthly_averages, seasonal_averages]
    )
    fig_averages.update_layout(
        title=f"Average rainfall (mm) between {begin_year} and {end_year}"
    )
    fig_averages.update_yaxes(title_text="Rainfall (mm)")

    monthly_linreg_slopes = api_client.get_rainfall_linreg_slopes_as_plotly_json(
        time_mode="monthly",
        begin_year=begin_year,
        end_year=end_year,
    )

    seasonal_linreg_slopes = api_client.get_rainfall_linreg_slopes_as_plotly_json(
        time_mode="seasonal",
        begin_year=begin_year,
        end_year=end_year,
    )

    fig_linreg_slopes = _aggregate_json_traces_as_figure(
        [monthly_linreg_slopes, seasonal_linreg_slopes]
    )
    fig_linreg_slopes.update_layout(
        title=f"Average linear regression slope (mm/year) between {begin_year} and {end_year}"
    )
    fig_linreg_slopes.update_yaxes(title_text="Linear regression slope (mm/year)")

    csv_data = (
        api_client.get_rainfall_by_year_as_csv(
            time_mode="monthly",
            begin_year=1995,
            end_year=2015,
            month="May",
        )
        .content.decode()
        .splitlines()
    )

    return render_template(
        "index.html",
        plotlyJSON=data,
        plotlyToggleJSON=fig_averages.to_json(),
        plotlyLinRegJSON=fig_linreg_slopes.to_json(),
        dataCSV=[csv_line.split(",") for csv_line in csv_data],
    )
