from src.core.utils.enums.time_modes import TimeMode


def test_time_modes() -> None:
    assert len(TimeMode) == 3

    for time_mode in TimeMode:
        assert isinstance(time_mode.value, str)
