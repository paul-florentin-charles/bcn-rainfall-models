"""
Provides MIME types for API purpose: body, parameters, result, etc.
"""

import mimetypes

from src.core.utils.enums.base_enum import BaseEnum


class MediaType(str, BaseEnum):
    """
    An Enum listing useful MIME types.
    """

    APP_JSON: str = mimetypes.types_map[".json"]
    TXT_CSV: str = mimetypes.types_map[".csv"]
    IMG_SVG: str = mimetypes.types_map[".svg"]
