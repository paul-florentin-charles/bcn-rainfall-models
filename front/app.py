import requests
from flask import Flask

app = Flask(__name__)


@app.route("/")
def average_rainfall():
    return requests.get(
        "http://127.0.0.1:8000/api/rainfall/average?time_mode=yearly&begin_year=1971&end_year=2023"
    ).json()
