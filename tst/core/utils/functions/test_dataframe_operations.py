from datetime import datetime

import pandas as pd

import src.core.utils.functions.dataframe_operations as df_opr
from src.core.utils.enums.labels import Label
from src.core.utils.enums.months import Month
from tst.core.models.test_yearly_rainfall import YEARLY_RAINFALL


class TestDataframeOperations:
    @staticmethod
    def test_get_rainfall_within_year_interval():
        begin_year = 1995
        end_year = 2015

        cropped_yearly_rainfall = df_opr.get_rainfall_within_year_interval(
            YEARLY_RAINFALL.data, begin_year=begin_year, end_year=end_year
        )

        assert len(cropped_yearly_rainfall) <= end_year - begin_year + 1

    @staticmethod
    def test_remove_column():
        removed = df_opr.remove_column(YEARLY_RAINFALL.data, Label.YEAR)

        assert Label.YEAR in YEARLY_RAINFALL.data.columns
        assert not removed

        YEARLY_RAINFALL.add_savgol_filter()
        removed = df_opr.remove_column(
            YEARLY_RAINFALL.data, Label.SAVITZKY_GOLAY_FILTER
        )

        assert Label.SAVITZKY_GOLAY_FILTER not in YEARLY_RAINFALL.data.columns
        assert removed

        YEARLY_RAINFALL.add_savgol_filter()

    @staticmethod
    def test_concat_columns():
        result = df_opr.concat_columns(
            [
                pd.DataFrame(data={"col1": [1, 2, 3]}),
                pd.DataFrame(data={"col2": [4, 5, 6]}),
            ]
        )

        assert isinstance(result, pd.DataFrame)
        assert all(column in result.columns for column in ["col1", "col2"])
        assert len(result) == 3

    @staticmethod
    def test_retrieve_rainfall_data_with_constraints():
        result = df_opr.retrieve_rainfall_data_with_constraints(
            YEARLY_RAINFALL.data,
            YEARLY_RAINFALL.starting_year,
            YEARLY_RAINFALL.round_precision,
            Month.MAY.get_rank(),
            Month.SEPTEMBER.get_rank(),
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) <= datetime.now().year - YEARLY_RAINFALL.starting_year + 1
