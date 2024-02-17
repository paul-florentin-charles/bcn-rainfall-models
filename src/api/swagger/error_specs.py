from typing import Dict, Any

from src.api.schemas import ApiError

bad_request_specs: Dict[str, Any] = {
    "description": 'Bad Request: error specific to API; check "message" field for information.',
    "schema": ApiError,
}
