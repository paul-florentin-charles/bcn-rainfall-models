from typing import Any

from src.api.schemas import ApiError

bad_request_specs: dict[str, Any] = {
    "description": 'Bad Request: error specific to API; check "message" field for information.',
    "schema": ApiError,
}
