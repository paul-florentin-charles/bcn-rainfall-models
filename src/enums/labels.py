from enum import Enum


class Label(str, Enum):
    YEAR: str = 'Year'
    RAINFALL: str = 'Rainfall'
    PERCENTAGE_OF_NORMAL: str = 'Percentage of normal'
    LINEAR_REGRESSION: str = 'Linear regression'
    SAVITZKY_GOLAY_FILTER: str = 'Savitzky–Golay filter'
