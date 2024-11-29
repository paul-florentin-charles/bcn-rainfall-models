"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
Work-in-progress!
"""

from flask import Flask, render_template

from webapp import api_client
from webapp.views import metrics

app = Flask(__name__)
app.register_blueprint(metrics)


@app.route("/")
def index():
    data = api_client.get_rainfall_by_year_as_plotly_json(
        time_mode="seasonal",
        begin_year=1971,
        season="spring",
        plot_average=True,
    )

    data_2 = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="monthly",
        begin_year=1991,
        end_year=2020,
    )

    data_3 = api_client.get_rainfall_averages_as_plotly_json(
        time_mode="seasonal",
        begin_year=1991,
        end_year=2020,
    )

    return render_template(
        "index.html", plotlyJSON=data, plotlyJSON_2=data_2, plotlyJSON_3=data_3
    )
