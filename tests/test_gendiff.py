import os

import pytest  # type: ignore

from gendiff.main import generate_diff

test_dir = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.join(test_dir, "test_data", "file1.json")
file2 = os.path.join(test_dir, "test_data", "file2.json")
file_result = os.path.join(test_dir, "test_data", "expected_diff_plain.txt")


@pytest.fixture(scope="module")
def expected_output() -> str:
    """Фикстура для чтения эталонного вывода из файла."""
    return open(file_result).read()


def test_flat_json_diff(expected_output):
    """Тестирует сравнение двух плоских JSON-файлов."""

    assert generate_diff(file1, file2) == expected_output