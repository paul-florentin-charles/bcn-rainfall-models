#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI to run FastAPI or Flask servers.
"""

import click
import uvicorn  # type: ignore

from back.api.app import fastapi_app
from config import Config
from webapp.app import flask_app


@click.group()
def run():
    """
    Run either FastAPI or Flask servers.
    """


@run.command()
def api():
    """
    Run FastAPI server.
    """
    config = Config()
    uvicorn.run("back.api.app:fastapi_app", **config.get_api_server_settings)


@run.command()
def webapp():
    """
    Run Flask server.
    """
    config = Config()
    flask_app.run(**config.get_webapp_server_settings)


if __name__ == "__main__":
    run()
