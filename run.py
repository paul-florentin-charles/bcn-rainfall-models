#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI to run FastAPI or Flask servers.
"""

import click
import uvicorn  # type: ignore

from config import Config
from webapp.app import flask_app


@click.group()
def run():
    """
    Run either FastAPI or Flask servers.
    """


@run.command()
@click.pass_context
def api(ctx):
    uvicorn.run("back.api.app:fastapi_app", **ctx.ensure_object(Config).get_api_server_settings)


@run.command()
@click.pass_context
def webapp(ctx):
    flask_app.run(**ctx.ensure_object(Config).get_webapp_server_settings)


if __name__ == "__main__":
    run()
