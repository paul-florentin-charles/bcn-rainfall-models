from src.api.schemas import ApiError

bad_request_specs: dict = {
    "description": 'Bad Request: error specific to API; check "message" field for information.',
    "schema": ApiError,
}
