from src.core.utils.enums.labels import Label


def test_labels():
    for label in Label:
        assert isinstance(label.value, str)
