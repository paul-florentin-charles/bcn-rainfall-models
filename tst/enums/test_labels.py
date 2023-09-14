# pylint: disable=missing-docstring

from src.core.utils.enums.labels import Label


def test_labels() -> None:
    for label in Label:
        assert isinstance(label.value, str)
