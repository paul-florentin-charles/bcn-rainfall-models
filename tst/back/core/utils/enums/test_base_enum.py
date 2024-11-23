from back.core.utils.enums import BaseEnum


def test_base_enum():
    class TestEnum(BaseEnum):
        FOX = 0
        DOG = 1
        CAT = 2

    assert set(TestEnum.names()) == {"FOX", "DOG", "CAT"}
    assert set(TestEnum.values()) == {0, 1, 2}
