import os

import pytest  # type: ignore

from gendiff.main import generate_diff

test_dir = os.path.dirname(os.path.abspath(__file__))

file1 = os.path.join(test_dir, "test_data", "file1.json")
file2 = os.path.join(test_dir, "test_data", "file2.json")
file_result = os.path.join(test_dir, "test_data", "expected_diff_plain.txt")


@pytest.fixture(scope="module")
def expected_output() -> str:
    """Фикстура для чтения эталонного вывода из файла"""
    return open(file_result).read()


def test_flat_json_diff(expected_output):
    """Тестирует сравнение двух корректных плоских JSON-файлов
    , переданные путями"""
    assert generate_diff(file1, file2) == expected_output


def test_generate_diff_with_json_objects():
    """Тестирует сравнение двух корректных плоских JSON-файлов
    , передавая JSON-объекты напрямую."""

    data1 = {
        "follow": True,
        "host": "hexlet.io",
        "timeout": 40
    }
    data2 = {
        "host": "hexlet.io",
        "timeout": 10,
        "verbose": False
    }

    result = """{
  - follow: true
    host: hexlet.io
  - timeout: 40
  + timeout: 10
  + verbose: false
}"""

    assert generate_diff(data1, data2) == result


def test_flat_json_diff_empty_files():
    """Тестирует сравнение двух пустых JSON-файлов"""
    empty_file1 = {}
    empty_file2 = {}

    assert generate_diff(empty_file1, empty_file2) == "{\n\n}"


def test_generate_diff_invalid_json_input():
    """Тестирует обработку некорректного JSON при передаче строки."""
    data1 = {"a": 1}
    invalid_json_string = '{"key": "value" # oops'

    assert generate_diff(data1, invalid_json_string) == (
        f"Ошибка: Файл не найден: {invalid_json_string}"
    )


def test_generate_diff_file_not_found_error():
    """Тестирует обработку отсутствия файла при передаче пути."""
    data1 = {"a": 1}
    non_existent_file_path = "non_existent_file.json"
    result_error = generate_diff(non_existent_file_path, data1)
    assert result_error == f"Ошибка: Файл не найден: {non_existent_file_path}"

    result_error_2 = generate_diff(data1, non_existent_file_path)
    assert result_error_2 == f"Ошибка: Файл не найден: {non_existent_file_path}"


def test_generate_diff_type_error():
    """Тестирует обработку некорректного типа входных данных."""
    data1 = {"a": 1}
    invalid_type_input = 123
    
    result_error = generate_diff(data1, invalid_type_input)
    assert result_error == (
        "Ошибка: Источник должен быть"
        " путем к файлу (str) или словарем (dict)"
    )
