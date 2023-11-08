#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=missing-function-docstring

"""
Run the Flask app from this file.
Currently developing the Swagger API using flasgger.
"""

from flasgger import Swagger, swag_from
from flask import Flask, jsonify, request, Response

import src.api.schemas as model
from src.api.swagger.rainfall import (average_specs, normal_specs,
                                      relative_distance_to_normal_specs,
                                      standard_deviation_specs)
from src.api.swagger.year import below_normal_specs, above_normal_specs
import src.api.swagger.parameters_specs as param
from src.core.models.all_rainfall import AllRainfall
from config import Config

cfg = Config()
all_rainfall = AllRainfall(cfg.get_dataset_url(),
                           cfg.get_start_year(),
                           cfg.get_rainfall_precision())

app = Flask(__name__)
swagger = Swagger(app, template_file=f"{cfg.get_api_doc_path()}/template.yaml")


@app.route(f"{swagger.template['basePath']}/rainfall/average")
@swag_from(average_specs.route_specs)
def average_rainfall() -> Response:
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_average_yearly_rainfall(begin_year, end_year)

    return jsonify(model.AverageYearlyRainfall().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


@app.route(f"{swagger.template['basePath']}/rainfall/normal")
@swag_from(normal_specs.route_specs)
def normal_rainfall() -> Response:
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    value: float = all_rainfall.yearly_rainfall.get_normal(begin_year)

    return jsonify(model.NormalYearlyRainfall().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": begin_year + 29
    }))


@app.route(f"{swagger.template['basePath']}/rainfall/relative_distance_to_normal")
@swag_from(relative_distance_to_normal_specs.route_specs)
def rainfall_relative_distance_to_normal() -> Response:
    normal_year: int = request.args.get(param.normal_year['name'],
                                        default=param.normal_year['default'],
                                        type=int)
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_relative_distance_from_normal(
        normal_year,
        begin_year,
        end_year
    )

    return jsonify(model.RelativeDistanceToNormalYearlyRainfall().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


@app.route(f"{swagger.template['basePath']}/rainfall/standard_deviation")
@swag_from(standard_deviation_specs.route_specs)
def standard_deviation() -> Response:
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_standard_deviation(begin_year, end_year)

    return jsonify(model.StandardDeviationYearlyRainfall().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


@app.route(f"{swagger.template['basePath']}/year/below_normal")
@swag_from(below_normal_specs.route_specs)
def years_below_normal() -> Response:
    normal_year: int = request.args.get(param.normal_year['name'],
                                        default=param.normal_year['default'],
                                        type=int)
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_years_below_normal(
        normal_year,
        begin_year,
        end_year
    )

    return jsonify(model.YearsBelowNormalSchema().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


@app.route(f"{swagger.template['basePath']}/year/above_normal")
@swag_from(above_normal_specs.route_specs)
def years_above_normal() -> Response:
    normal_year: int = request.args.get(param.normal_year['name'],
                                        default=param.normal_year['default'],
                                        type=int)
    begin_year: int = request.args.get(param.begin_year['name'],
                                       default=param.begin_year['default'],
                                       type=int)
    end_year: int = request.args.get(param.end_year['name'],
                                     default=param.end_year['default'],
                                     type=int)
    value: float = all_rainfall.yearly_rainfall.get_years_above_normal(
        normal_year,
        begin_year,
        end_year
    )

    return jsonify(model.YearsAboveNormalSchema().load({
        "value": value,
        "begin_year": begin_year,
        "end_year": end_year,
    }))


if __name__ == '__main__':
    app.run(debug=True)
