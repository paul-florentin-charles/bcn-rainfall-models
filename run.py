#!/usr/bin/env python

"""
CLI to run FastAPI or Flask servers.
"""

import click
import uvicorn  # type: ignore


@click.group()
def run():
    """
    Run either FastAPI or Flask servers.
    """


@run.command()
@click.pass_context
def api(ctx):
    from back.api.config import Config

    uvicorn.run(
        "back.api.app:fastapi_app",
        **ctx.ensure_object(Config).get_api_settings.server.model_dump(),
    )


@run.command()
@click.pass_context
def webapp(ctx):
    from webapp.app import flask_app
    from webapp.config import Config

    flask_app.run(**ctx.ensure_object(Config).get_webapp_server_settings.model_dump())


if __name__ == "__main__":
    run()
