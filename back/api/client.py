"""
API client built to interact with FastAPI application without needing the knowledge of the routes URLs.
"""

from typing import Any

from api_session import APISession

from config import Config


class APIClient(APISession):
    @classmethod
    def from_config(cls, **kwargs):
        settings = Config().get_api_server_settings()
        base_url = f"http://{settings['host']}:{settings['port']}/api"

        return cls(base_url, **kwargs)

    def get_rainfall_average(
        self,
        *,
        time_mode: str,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/rainfall/average",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month,
                "season": season,
            },
        )

    def get_rainfall_normal(
        self,
        *,
        time_mode: str,
        begin_year: int,
        month: str | None = None,
        season: str | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/rainfall/normal",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "month": month,
                "season": season,
            },
        )

    def get_rainfall_relative_distance_to_normal(
        self,
        *,
        time_mode: str,
        begin_year: int,
        normal_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/rainfall/relative_distance_to_normal",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "normal_year": normal_year,
                "end_year": end_year,
                "month": month,
                "season": season,
            },
        )

    def get_rainfall_standard_deviation(
        self,
        *,
        time_mode: str,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
        weigh_by_average=False,
    ):
        return self.get_json_api(
            "/rainfall/standard_deviation",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month,
                "season": season,
                "weigh_by_average": weigh_by_average,
            },
        )

    def get_years_below_normal(
        self,
        *,
        time_mode: str,
        normal_year: int,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/year/below_normal",
            params={
                "time_mode": time_mode,
                "normal_year": normal_year,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month,
                "season": season,
            },
        )

    def get_years_above_normal(
        self,
        *,
        time_mode: str,
        normal_year: int,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ) -> dict[str, Any]:
        return self.get_json_api(
            "/year/above_normal",
            params={
                "time_mode": time_mode,
                "normal_year": normal_year,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month,
                "season": season,
            },
        )

    def get_rainfall_by_year_as_csv(
        self,
        time_mode: str,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
    ):
        return self.get_api(
            "/csv/rainfall_by_year",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month,
                "season": season,
            },
        )

    def get_rainfall_by_year_as_plotly_json(
        self,
        *,
        time_mode: str,
        begin_year: int,
        end_year: int | None = None,
        month: str | None = None,
        season: str | None = None,
        plot_average=False,
    ) -> str:
        return self.get_json_api(
            "/graph/rainfall_by_year",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "end_year": end_year,
                "month": month,
                "season": season,
                "plot_average": plot_average,
                "as_json": True,
            },
        )

    def get_rainfall_averages_as_plotly_json(
        self,
        *,
        time_mode: str,
        begin_year: int,
        end_year: int | None = None,
    ) -> str:
        return self.get_json_api(
            "/graph/rainfall_averages",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "end_year": end_year,
                "as_json": True,
            },
        )

    def get_rainfall_linreg_slopes_as_plotly_json(
        self,
        *,
        time_mode: str,
        begin_year: int,
        end_year: int | None = None,
    ) -> str:
        return self.get_json_api(
            "/graph/rainfall_linreg_slopes",
            params={
                "time_mode": time_mode,
                "begin_year": begin_year,
                "end_year": end_year,
                "as_json": True,
            },
        )
