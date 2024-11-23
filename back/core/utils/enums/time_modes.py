"""
Provides list of Time modes (Enum) to inform on what timeframe is used on current rainfall data.
"""

from back.core.utils.enums import BaseEnum


class TimeMode(BaseEnum):
    """
    An enum listing time modes (yearly, monthly and seasonal) represented by strings.
    """

    YEARLY = "yearly"
    SEASONAL = "seasonal"
    MONTHLY = "monthly"
