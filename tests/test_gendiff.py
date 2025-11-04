import io
import sys

import pytest

from gendiff.scripts.gendiff import main


def test_main_output(monkeypatch):
    """Тестирует успешное выполнение main() с двумя файлами."""
    captured_output = io.StringIO()
    monkeypatch.setattr(sys, 'stdout', captured_output)

    original_argv = sys.argv
    sys.argv = ['gendiff', 'file1.json', 'file2.json', '-f', 'json']

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

    expected_output = (
        "usage: gendiff [-h] [-f FORMAT] first_file second_file\n\n"
        "Compares two configuration files and shows a difference.\n\n"
        "positional arguments:\n"
        "  first_file\n"
        "  second_file\n\n"
        "options:\n"
        "  -h, --help           show this help message and exit\n"
        "  -f, --format FORMAT  set format of output"
    )

    assert captured_output.getvalue().strip() == expected_output

