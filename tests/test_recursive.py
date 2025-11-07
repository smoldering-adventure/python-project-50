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


def test_plain_format_still_works():
    """Тестирует что plain формат все еще работает для плоских структур."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({"key": "value1"}, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({"key": "value2"}, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'plain')
        assert "Property 'key' was updated. From 'value1' to 'value2'" in result
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)


def test_plain_format_with_nested():
    """Тестирует plain формат с вложенными структурами."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({"parent": {"child": "value1"}}, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({"parent": {"child": "value2"}}, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'plain')
        # Проверяем plain формат с вложенными структурами
        assert "Property 'parent.child' was updated. From 'value1' to 'value2'" in result
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)