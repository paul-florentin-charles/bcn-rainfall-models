from flask import Flask

from back.api import APIClient
from back.core.utils.enums.time_modes import TimeMode
from back.core.utils.enums.months import Month

app = Flask(__name__)

api_client = APIClient.from_config()


@app.route("/")
def average_rainfall():
    return api_client.get_rainfall_average(
        time_mode=TimeMode.YEARLY, begin_year=1991, end_year=2021
    )


@app.route("/normal")
def normal_rainfall():
    return api_client.get_rainfall_normal(
        time_mode=TimeMode.MONTHLY, begin_year=1985, month=Month.MAY
    )
