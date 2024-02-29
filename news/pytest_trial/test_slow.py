import pytest
from time import sleep


@pytest.mark.slow  # Отмечаем маркером тест.
def test_type():
    """Тестируем тип данных, возвращаемых из get_sort_list()."""
    sleep(3)


# @pytest.mark.slowww  # Название маркера с опечаткой.
# def test_type():