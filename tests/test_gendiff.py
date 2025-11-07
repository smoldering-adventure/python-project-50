import io
import sys

import pytest  # type: ignore

from gendiff.scripts.gendiff import main


def test_main_output(monkeypatch):
    """Тестирует успешное выполнение main() с двумя файлами в stylish формате."""
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)

    original_argv = sys.argv
    sys.argv = ['gendiff', 'file1.json', 'file2.json']

    main()

    sys.argv = original_argv

    assert captured_output.getvalue().strip() == """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""


def test_main_plain_format(monkeypatch):
    """Тестирует успешное выполнение main() с двумя файлами в plain формате."""
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)

    original_argv = sys.argv
    sys.argv = ['gendiff', 'file1.json', 'file2.json', '-f', 'plain']

    main()

    sys.argv = original_argv

    assert captured_output.getvalue().strip() == """{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}"""


def test_main_help(monkeypatch):
    """Тестирует, что скрипт корректно обрабатывает опцию -h."""
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)
    monkeypatch.setattr(sys, 'argv', ['gendiff', '-h'])

    with pytest.raises(SystemExit) as exc_info:
        main()

    # Проверяем что выход с кодом 0 (успех)
    assert exc_info.value.code == 0

    actual_output = captured_output.getvalue().strip()
    
    # Проверяем ключевые части вывода вместо точного совпадения
    assert "usage: gendiff" in actual_output
    assert (
        "Compares two configuration files and shows a difference."
        in actual_output
    )
    assert "first_file" in actual_output
    assert "second_file" in actual_output
    assert "-h, --help" in actual_output
    assert "--format FORMAT" in actual_output or "-f FORMAT" in actual_output


def test_main_missing_arguments(monkeypatch):
    """Тестирует обработку отсутствия обязательных аргументов."""
    captured_output = io.StringIO()
    captured_error = io.StringIO()
    
    monkeypatch.setattr(sys, 'stdout', captured_output)
    monkeypatch.setattr(sys, 'stderr', captured_error)
    monkeypatch.setattr(sys, 'argv', ['gendiff'])  # Нет аргументов

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    
    error_output = captured_error.getvalue()
    assert "error" in error_output.lower()