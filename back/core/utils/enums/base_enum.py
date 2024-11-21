"""
Provides a custom Enum that should be inherited from instead of Enum.
"""

from enum import Enum


class BaseEnum(Enum):
    """
    Same as Enum but with some handy class methods.
    """

    @classmethod
    def names(cls):
        """
        Retrieve all names from an Enum.

        :return: A list made of the Enum names.
        """
        return [enum.name for enum in cls]

    @classmethod
    def values(cls):
        """
        Retrieve all values from an Enum.

        :return: A list made of the Enum values.
        """
        return [enum.value for enum in cls]
