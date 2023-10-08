"""
Provides tuples to easily retrieve parameters in API requests.
"""

from enum import Enum


class Parameter(tuple, Enum):
    """
    An Enum listing API parameters as tuples.
    Format: (name, default_value [nullable], type [nullable])
    Unpack these with * in request arguments dict.
    """
    BEGIN_YEAR: tuple = ('begin_year', None, int)
    END_YEAR: tuple = ('end_year', None, int)
    NORMAL: tuple = ('normal', None, float)
    NORMAL_YEAR: tuple = ('normal_year', None, int)
