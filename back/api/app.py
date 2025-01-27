"""
FastAPI application exposing API routes related to rainfall data of Barcelona.
"""
from typing import Any, Callable

from fastapi import FastAPI

from back.api.routes import (
    MAX_YEAR_AVAILABLE,
    MIN_YEAR_AVAILABLE,
    _get_endpoint_to_api_route_specs,
)
from config import Config


class FastAPPI(FastAPI):
    """Overrides FastAPI class to initiate our own app."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for endpoint, api_route_specs in _get_endpoint_to_api_route_specs().items():
            self.add_api_route(
                endpoint=endpoint,
                **api_route_specs,
            )

    @classmethod
    def from_config(cls, config: dict[str, Any] | None = None):
        if config is None:
            config = Config()

        return cls(
            **config.get_fastapi_settings(),
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
