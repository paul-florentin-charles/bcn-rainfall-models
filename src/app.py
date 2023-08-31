"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""

from flasgger import Swagger
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
def average_rainfall() -> Response:
    """Retrieve average rainfall for Barcelona between two years.
    Only the starting year is compulsory.
    If no ending year is precised, computes average until most recent year available.
    ---
    tags:
      - rainfall
    parameters:
      - name: begin_year
        in: query
        type: integer
        required: true
        default: 1970
      - name: end_year
        in: query
        type: integer
        required: false
        default: 2020
    responses:
      200:
        description: the average rainfall
        content:
          application/json:
            schema:
              type: integer
    """
    begin_year: int = request.args.get('begin_year', type=int)
    end_year: int = request.args.get('end_year', type=int)

    return jsonify(all_rainfall.yearly_rainfall.get_average_yearly_rainfall(
        begin_year,
        end_year
    ))


@app.route('/year/below_normal')
def years_below_normal() -> Response:
    """Computes the number of years below normal for a specific year range.
    Only the starting year is compulsory.
    If normal is set to None, it will be computed as a 30 years average
    starting from the starting year set in configuration.
    ---
    tags:
      - year
    parameters:
      - name: normal
        in: query
        type: number
        required: false
      - name: begin_year
        in: query
        type: integer
        required: true
        default: 1970
      - name: end_year
        in: query
        type: integer
        required: false
        default: 2020
    responses:
      200:
        description: the number of years below normal
        content:
          application/json:
            schema:
              type: integer
    """
    normal: float = request.args.get('normal', type=float)
    begin_year: int = request.args.get('begin_year', type=int)
    end_year: int = request.args.get('end_year', type=int)

    return jsonify(all_rainfall.yearly_rainfall.get_years_below_normal(
        normal,
        begin_year,
        end_year
    ))


@app.route('/year/above_normal')
def years_above_normal() -> Response:
    """Computes the number of years above normal for a specific year range.
    Only the starting year is compulsory.
    If normal is set to None, it will be computed as a 30 years average
    starting from the starting year set in configuration.
    ---
    tags:
      - year
    parameters:
      - name: normal
        in: query
        type: number
        required: false
      - name: begin_year
        in: query
        type: integer
        required: true
        default: 1970
      - name: end_year
        in: query
        type: integer
        required: false
        default: 2020
    responses:
      200:
        description: the number of years above normal
        content:
          application/json:
            schema:
              type: integer
    """
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
