# pylint: disable=missing-docstring

from pathlib import Path
from shutil import rmtree

from tst.models.test_yearly_rainfall import all_rainfall


def test_export_all_data_to_csv() -> None:
    folder_path: str = all_rainfall.export_all_data_to_csv()

    assert isinstance(folder_path, str)
    assert Path(folder_path).exists()

    rmtree(folder_path)
