#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple python script to either run API with Uvicorn or Webapp with Flask.
"""

import click
import uvicorn


SERVERS = ["api", "webapp"]


@click.command()
@click.argument(
    "server",
    type=click.Choice(SERVERS, case_sensitive=False),
)
def run(server: str):
    from config import Config

    config = Config()
    match server:
        case "api":
            uvicorn.run("back.api.app:fastapi_app", **config.get_api_server_settings())
        case "webapp":
            from webapp.app import flask_app

            flask_app.run(**config.get_webapp_server_settings())
        case _:  # Should not happen
            click.echo(f"Argument should be in {SERVERS} (case-insensitive)")
            exit(1)


if __name__ == "__main__":
    run()
