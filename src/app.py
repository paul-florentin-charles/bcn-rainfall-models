# pylint: disable=missing-function-docstring

"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""

from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response

from src.classes.all_rainfall import AllRainfall
from src.config import Config

cfg = Config()
all_rainfall = AllRainfall(cfg.get_dataset_url(),
                           cfg.get_start_year(),
                           cfg.get_rainfall_precision())

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/rainfall/average')
@swag_from('swagger/rainfall/average.yaml')
def average_rainfall() -> Response:
    begin_year: int = request.args.get('begin_year', type=int)
    end_year: int = request.args.get('end_year', type=int)

    return jsonify(all_rainfall.yearly_rainfall.get_average_yearly_rainfall(
        begin_year,
        end_year
    ))


@app.route('/rainfall/normal')
@swag_from('swagger/rainfall/normal.yaml')
def normal_rainfall() -> Response:
    begin_year: int = request.args.get('begin_year', type=int)

    return jsonify(all_rainfall.yearly_rainfall.get_normal(begin_year))


@app.route('/year/below_normal')
@swag_from('swagger/year/below_normal.yaml')
def years_below_normal() -> Response:
    normal: float = request.args.get('normal', type=float)
    begin_year: int = request.args.get('begin_year', type=int)
    end_year: int = request.args.get('end_year', type=int)

    return jsonify(all_rainfall.yearly_rainfall.get_years_below_normal(
        normal,
        begin_year,
        end_year
    ))


@app.route('/year/above_normal')
@swag_from('swagger/year/above_normal.yaml')
def years_above_normal() -> Response:
    normal: float = request.args.get('normal', type=float)
    begin_year: int = request.args.get('begin_year', type=int)
    end_year: int = request.args.get('end_year', type=int)

    return jsonify(all_rainfall.yearly_rainfall.get_years_above_normal(
        normal,
        begin_year,
        end_year
    ))


if __name__ == '__main__':
    app.run(debug=True)
