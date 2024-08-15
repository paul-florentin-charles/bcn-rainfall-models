"""
Provides MIME types for API purpose: body, parameters, result, etc.
"""

import mimetypes

from src.core.utils.enums.base_enum import BaseEnum


class MediaType(BaseEnum):
    """
    An Enum listing useful MIME types.
    """

    TXT_CSV = mimetypes.types_map[".csv"]
    IMG_PNG = mimetypes.types_map[".png"]
