"""
FastAPI application exposing API routes related to rainfall data of Barcelona.
"""

from typing import Any, Callable

from fastapi import FastAPI


class FastAPPI(FastAPI):
    """Overrides FastAPI class to initiate our own app."""

    def __init__(self, **kwargs):
        from back.api.routes import get_endpoint_to_api_route_specs

        super().__init__(**kwargs)

        for endpoint, api_route_specs in get_endpoint_to_api_route_specs().items():
            self.add_api_route(
                endpoint=endpoint,
                **api_route_specs.model_dump(),
            )

    @classmethod
    def from_config(cls):
        from back.api.routes import MAX_YEAR_AVAILABLE, MIN_YEAR_AVAILABLE
        from config import Config

        return cls(
            **Config().get_api_settings.fastapi.model_dump(),
            description=f"Available data is between {MIN_YEAR_AVAILABLE} and {MAX_YEAR_AVAILABLE}.",
        )

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        **kwargs,
    ):
        kwargs.setdefault("methods", ["GET"])
        kwargs.setdefault("operation_id", endpoint.__name__.title().replace("_", ""))

        super().add_api_route(path, endpoint, **kwargs)


fastapi_app = FastAPPI.from_config()
