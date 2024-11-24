from typing import Any

from api_session import APISession

from back.core.utils.enums.months import Month
from back.core.utils.enums.seasons import Season
from back.core.utils.enums.time_modes import TimeMode
from config import Config


class APIClient(APISession):
    @classmethod
    def from_config(cls, **kwargs):
        settings = Config().get_api_server_settings()
        base_url = f"http://{settings['host']}:{settings['port']}/api"

        return cls(base_url, **kwargs)

    def get_rainfall_average(
        self,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int | None = None,
        month: Month | None = None,
        season: Season | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/rainfall/average",
            params={
                "time_mode": time_mode.value,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month.value if month else None,
                "season": season.value if season else None,
            },
        )

    def get_rainfall_normal(
        self,
        time_mode: TimeMode,
        begin_year: int,
        month: Month | None = None,
        season: Season | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/rainfall/normal",
            params={
                "time_mode": time_mode.value,
                "begin_year": begin_year,
                "month": month.value if month else None,
                "season": season.value if season else None,
            },
        )

    def get_rainfall_relative_distance_to_normal(
        self,
        time_mode: TimeMode,
        begin_year: int,
        normal_year: int,
        end_year: int | None = None,
        month: Month | None = None,
        season: Season | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/rainfall/relative_distance_to_normal",
            params={
                "time_mode": time_mode.value,
                "begin_year": begin_year,
                "normal_year": normal_year,
                "end_year": end_year,
                "month": month.value if month else None,
                "season": season.value if season else None,
            },
        )

    def get_rainfall_standard_deviation(
        self,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int | None = None,
        month: Month | None = None,
        season: Season | None = None,
        weigh_by_average=False,
    ):
        return self.get_json_api(
            "/rainfall/standard_deviation",
            params={
                "time_mode": time_mode.value,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month.value if month else None,
                "season": season.value if season else None,
                "weigh_by_average": weigh_by_average,
            },
        )

    def get_rainfall_by_year_as_plotly_json(
        self,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int | None = None,
        month: Month | None = None,
        season: Season | None = None,
        plot_average=False,
    ) -> dict:
        return self.get_json_api(
            "/graph/rainfall_by_year",
            params={
                "time_mode": time_mode.value,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month.value if month else None,
                "season": season.value if season else None,
                "plot_average": plot_average,
                "as_json": True,
            },
        )
