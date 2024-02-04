from datetime import datetime

import pandas as pd

import src.core.utils.functions.dataframe_operations as df_opr
from src.core.utils.enums.labels import Label
from src.core.utils.enums.months import Month
from tst.core.models.test_yearly_rainfall import yearly_rainfall


class TestDataframeOperations:
    @staticmethod
    def test_get_rainfall_within_year_interval() -> None:
        begin_year: int = 1995
        end_year: int = 2015
        cropped_yearly_rainfall: pd.DataFrame = (
            df_opr.get_rainfall_within_year_interval(
                yearly_rainfall.data, begin_year, end_year
            )
        )

        assert len(cropped_yearly_rainfall) <= end_year - begin_year + 1

    @staticmethod
    def test_remove_column() -> None:
        removed: bool = df_opr.remove_column(yearly_rainfall.data, Label.YEAR)

        assert Label.YEAR in yearly_rainfall.data.columns
        assert not removed

        yearly_rainfall.add_savgol_filter()
        removed = df_opr.remove_column(
            yearly_rainfall.data, Label.SAVITZKY_GOLAY_FILTER
        )

        assert Label.SAVITZKY_GOLAY_FILTER not in yearly_rainfall.data.columns
        assert removed

        yearly_rainfall.add_savgol_filter()

    @staticmethod
    def test_concat_columns() -> None:
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
    def test_retrieve_rainfall_data_with_constraints() -> None:
        result: pd.DataFrame = df_opr.retrieve_rainfall_data_with_constraints(
            yearly_rainfall.data,
            yearly_rainfall.starting_year,
            yearly_rainfall.round_precision,
            Month.MAY.value,
            Month.SEPTEMBER.value,
        )

        assert isinstance(result, pd.DataFrame)
        assert len(result) <= datetime.now().year - yearly_rainfall.starting_year + 1
