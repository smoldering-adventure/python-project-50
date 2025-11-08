import os
import tempfile

from gendiff.main import generate_diff

test_dir = os.path.dirname(os.path.abspath(__file__))


def test_flat_yaml_diff():
    """Тестирует сравнение двух плоских YAML-файлов."""
    yaml_file1 = os.path.join(test_dir, "test_data", "file1.yaml")
    yaml_file2 = os.path.join(test_dir, "test_data", "file2.yaml")
    
    result = generate_diff(yaml_file1, yaml_file2)
    
    # Проверяем ожидаемый вывод
    assert "  - follow: false" in result
    assert "    host: hexlet.io" in result
    assert "  - proxy: 123.234.53.22" in result
    assert "  - timeout: 50" in result
    assert "  + timeout: 20" in result
    assert "  + verbose: true" in result


def test_yaml_and_json_comparison():
    """Тестирует что YAML и JSON 
    с одинаковыми данными дают одинаковый результат."""
    json_file1 = os.path.join(test_dir, "test_data", "file1.json")
    json_file2 = os.path.join(test_dir, "test_data", "file2.json")
    yaml_file1 = os.path.join(test_dir, "test_data", "file1.yaml")
    yaml_file2 = os.path.join(test_dir, "test_data", "file2.yaml")
    
    json_result = generate_diff(json_file1, json_file2)
    yaml_result = generate_diff(yaml_file1, yaml_file2)
    
    assert json_result == yaml_result


def test_yaml_file_not_found():
    """Тестирует обработку отсутствующих YAML файлов."""
    result = generate_diff("nonexistent.yaml", "nonexistent2.yaml")
    assert "Ошибка: Файл не найден: nonexistent.yaml" in result


def test_invalid_yaml_file():
    """Тестирует обработку некорректного YAML файла."""
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.yaml', delete=False
    ) as f:
        f.write("invalid: yaml: content: [")
        invalid_yaml = f.name
    
    try:
        result = generate_diff(invalid_yaml, invalid_yaml)
        assert "Ошибка: Некорректный YAML в файле" in result
    finally:
        import os
        os.unlink(invalid_yaml)