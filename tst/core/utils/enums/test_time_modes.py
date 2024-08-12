from src.core.utils.enums.time_modes import TimeMode


def test_time_modes():
    assert len(TimeMode) == 3

    for t_mode in TimeMode.values():
        assert isinstance(t_mode, str)
