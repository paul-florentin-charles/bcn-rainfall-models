"""
Webapp run with Flask that communicates with an API (FastAPI/Uvicorn) to display rainfall-related data.
/!\ WIP /!\
"""

from flask import Flask

from back.api import APIClient
from back.core.utils.enums.seasons import Season
from back.core.utils.enums.time_modes import TimeMode
from back.core.utils.enums.months import Month

app = Flask(__name__)

api_client = APIClient.from_config()


@app.route("/average")
def rainfall_average():
    return api_client.get_rainfall_average(
        time_mode=TimeMode.YEARLY, begin_year=1991, end_year=2021
    )


@app.route("/normal")
def rainfall_normal():
    return api_client.get_rainfall_normal(
        time_mode=TimeMode.MONTHLY, begin_year=1985, month=Month.MAY
    )


@app.route("/")
def rainfall_relative_distance_to_normal():
    return api_client.get_rainfall_relative_distance_to_normal(
        time_mode=TimeMode.SEASONAL,
        begin_year=1995,
        normal_year=1975,
        season=Season.FALL,
    )
