"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

from flask import Flask, render_template
import plotly.graph_objs as go
from plotly.io import from_json

from webapp import api_client
from webapp.views import metrics

flask_app = Flask(__name__)
flask_app.register_blueprint(metrics)


@flask_app.route("/")
def index():
    data = api_client.get_rainfall_by_year_as_plotly_json(
        time_mode="seasonal",
        begin_year=1971,
        season="spring",
        plot_average=True,
    )

    begin_year = 1991
    end_year = 2020
    data_2 = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="monthly",
        begin_year=begin_year,
        end_year=end_year,
    )

    data_3 = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="seasonal",
        begin_year=begin_year,
        end_year=end_year,
    )

    figure = go.Figure()
    figure.add_trace(list(from_json(data_2).select_traces())[0])
    figure.add_trace(list(from_json(data_3).select_traces())[0])
    figure.update_layout(
        title=f"Average rainfall (mm) between {begin_year} and {end_year}"
    )
    figure.update_xaxes(title_text="Season | Month")

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
        plotlyJSON_2=data_2,
        plotlyJSON_3=data_3,
        plotlyToggleJSON=figure.to_json(),
        dataCSV=[csv_line.split(",") for csv_line in csv_data],
    )
