import json
import os
import tempfile

from gendiff.main import generate_diff

test_dir = os.path.dirname(os.path.abspath(__file__))


def test_recursive_json_diff():
    """Тестирует рекурсивное сравнение JSON файлов."""
    json_file1 = os.path.join(test_dir, "test_data", "file1_recursive.json")
    json_file2 = os.path.join(test_dir, "test_data", "file2_recursive.json")
    
    result = generate_diff(json_file1, json_file2, 'stylish')
    
    # Проверяем ключевые элементы вывода
    assert "common: {" in result
    assert "+ follow: false" in result
    assert "setting1: Value 1" in result
    assert "- setting2: 200" in result
    assert "- setting3: true" in result
    assert "+ setting3: null" in result
    assert "group1: {" in result
    assert "- baz: bas" in result
    assert "+ baz: bars" in result
    assert "- group2: {" in result
    assert "+ group3: {" in result


def test_recursive_yaml_diff():
    """Тестирует рекурсивное сравнение YAML файлов."""
    yaml_file1 = os.path.join(test_dir, "test_data", "file1_recursive.yaml")
    yaml_file2 = os.path.join(test_dir, "test_data", "file2_recursive.yaml")
    
    result = generate_diff(yaml_file1, yaml_file2, 'stylish')
    
    # Должен быть такой же результат как для JSON
    assert "common: {" in result
    assert "+ follow: false" in result
    assert "- setting2: 200" in result


def test_json_and_yaml_recursive_comparison():
    """Тестирует что YAML и JSON с одинаковыми данными дают одинаковый результат."""
    json_file1 = os.path.join(test_dir, "test_data", "file1_recursive.json")
    json_file2 = os.path.join(test_dir, "test_data", "file2_recursive.json")
    yaml_file1 = os.path.join(test_dir, "test_data", "file1_recursive.yaml")
    yaml_file2 = os.path.join(test_dir, "test_data", "file2_recursive.yaml")
    
    json_result = generate_diff(json_file1, json_file2, 'stylish')
    yaml_result = generate_diff(yaml_file1, yaml_file2, 'stylish')
    
    assert json_result == yaml_result


def test_default_format_is_stylish():
    """Тестирует что по умолчанию используется stylish формат."""
    json_file1 = os.path.join(test_dir, "test_data", "file1_recursive.json")
    json_file2 = os.path.join(test_dir, "test_data", "file2_recursive.json")
    
    result_default = generate_diff(json_file1, json_file2)
    result_stylish = generate_diff(json_file1, json_file2, 'stylish')
    
    assert result_default == result_stylish


def test_plain_format_flat_files():
    """Тестирует plain формат для плоских файлов."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({
            "follow": False,
            "host": "hexlet.io",
            "proxy": "192.168.1.1",
            "timeout": 50
        }, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({
            "host": "hexlet.io",
            "timeout": 20,
            "verbose": True
        }, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'plain')
        
        expected_lines = [
            "Property 'follow' was removed",
            "Property 'proxy' was removed", 
            "Property 'timeout' was updated. From 50 to 20",
            "Property 'verbose' was added with value: true"
        ]
        
        for line in expected_lines:
            assert line in result
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)


def test_plain_format_recursive():
    """Тестирует plain формат для рекурсивных структур."""
    file1 = os.path.join(test_dir, "test_data", "file1_recursive.json")
    file2 = os.path.join(test_dir, "test_data", "file2_recursive.json")
    
    result = generate_diff(file1, file2, 'plain')
    
    expected_lines = [
        "Property 'common.follow' was added with value: false",
        "Property 'common.setting2' was removed",
        "Property 'common.setting3' was updated. From true to null",
        "Property 'common.setting4' was added with value: 'blah blah'",
        "Property 'common.setting5' was added with value: [complex value]",
        "Property 'common.setting6.doge.wow' was updated. From '' to 'so much'",
        "Property 'common.setting6.ops' was added with value: 'vops'",
        "Property 'group1.baz' was updated. From 'bas' to 'bars'",
        "Property 'group1.nest' was updated. From [complex value] to 'str'",
        "Property 'group2' was removed",
        "Property 'group3' was added with value: [complex value]"
    ]
    
    for line in expected_lines:
        assert line in result


def test_plain_format_complex_values():
    """Тестирует отображение сложных значений как [complex value]."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({
            "nested": {"key": "value"}
        }, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({
            "nested": {"key": "new_value", "new_key": "value"}
        }, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'plain')
        
        assert "Property 'nested.key' was updated. From 'value' to 'new_value'" in result
        assert "Property 'nested.new_key' was added with value: 'value'" in result
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)


def test_plain_format_empty_files():
    """Тестирует plain формат для пустых файлов."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({}, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({}, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'plain')
        assert result == ""  # Для одинаковых пустых файлов - пустой вывод
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)