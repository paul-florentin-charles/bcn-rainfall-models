# pylint: disable=missing-docstring

import pandas as pd

import core.utils.functions.dataframe_operations as df_opr
from core.utils.enums.labels import Label

from tst.models.test_yearly_rainfall import yearly_rainfall


class TestDataframeOperations:
    @staticmethod
    def test_get_rainfall_within_year_interval() -> None:
        begin_year: int = 1995
        end_year: int = 2015
        cropped_yearly_rainfall: pd.DataFrame = df_opr.get_rainfall_within_year_interval(
            yearly_rainfall.data,
            begin_year,
            end_year
        )

        assert len(cropped_yearly_rainfall) <= end_year - begin_year + 1

    @staticmethod
    def test_remove_column() -> None:
        removed: bool = df_opr.remove_column(yearly_rainfall.data, Label.YEAR)

        assert Label.YEAR in yearly_rainfall.data.columns
        assert not removed

        yearly_rainfall.add_savgol_filter()
        removed = df_opr.remove_column(yearly_rainfall.data, Label.SAVITZKY_GOLAY_FILTER)

        assert Label.SAVITZKY_GOLAY_FILTER not in yearly_rainfall.data.columns
        assert removed

        yearly_rainfall.add_savgol_filter()
