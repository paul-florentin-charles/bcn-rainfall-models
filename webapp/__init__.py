from back.api import APIClient

api_client = APIClient.from_config()

NORMAL_YEAR = 1981
BEGIN_YEAR = 1994
END_YEAR = 2024

__all__ = ["api_client", "NORMAL_YEAR", "BEGIN_YEAR", "END_YEAR"]
