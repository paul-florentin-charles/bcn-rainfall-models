"""
Provides list of Time modes (Enum) to inform on what timeframe is used on current rainfall data.
"""

from src.core.utils.enums.base_enum import BaseEnum


class TimeMode(str, BaseEnum):
    """
    An enum listing time modes (yearly, monthly and seasonal) represented by strings.
    """

    YEARLY: str = "yearly"
    SEASONAL: str = "seasonal"
    MONTHLY: str = "monthly"
