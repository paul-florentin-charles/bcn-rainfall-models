#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple python script to either run API with Uvicorn or Webapp with Flask.
"""

import click
import uvicorn

from config import Config

SERVERS = ["api", "webapp"]


@click.command()
@click.option(
    "--server",
    "-s",
    type=click.Choice(SERVERS, case_sensitive=False),
    help="The server that should be run.",
)
def run(server: str):
    config = Config()
    match server:
        case "api":
            uvicorn.run("back.api.routes:app", **config.get_api_server_settings())
        case "webapp":
            from webapp import app

            app.run(**config.get_webapp_server_settings())
        case _:  # Should not happen
            click.echo(f"Option --server/-s should be in {SERVERS} (case-insensitive)")
            exit(1)


if __name__ == "__main__":
    run()
