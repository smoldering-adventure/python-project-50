import json
import os
import tempfile

from gendiff.main import generate_diff

test_dir = os.path.dirname(os.path.abspath(__file__))


def test_json_format_flat_files():
    """Тестирует JSON формат для плоских файлов."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({
            "follow": False,
            "host": "hexlet.io",
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
        result = generate_diff(file1, file2, 'json')
        
        # Проверяем что результат является валидным JSON
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        
        # Проверяем структуру JSON вывода
        for item in parsed_result:
            assert 'key' in item
            assert 'type' in item
            assert item['type'] in ['added', 'removed', 'unchanged', 'changed', 'nested']
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)


def test_json_format_recursive():
    """Тестирует JSON формат для рекурсивных структур."""
    file1 = os.path.join(test_dir, "test_data", "file1_recursive.json")
    file2 = os.path.join(test_dir, "test_data", "file2_recursive.json")
    
    result = generate_diff(file1, file2, 'json')
    
    # Проверяем что результат является валидным JSON
    parsed_result = json.loads(result)
    assert isinstance(parsed_result, list)
    
    # Проверяем наличие ключевых узлов
    keys = [item['key'] for item in parsed_result]
    assert 'common' in keys
    assert 'group1' in keys


def test_json_format_contains_correct_structure():
    """Тестирует что JSON формат содержит правильную структуру данных."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({"key": "value1"}, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({"key": "value2"}, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'json')
        parsed_result = json.loads(result)
        
        # Должен быть один элемент с типом 'changed'
        assert len(parsed_result) == 1
        node = parsed_result[0]
        assert node['key'] == 'key'
        assert node['type'] == 'changed'
        assert node['old_value'] == 'value1'
        assert node['new_value'] == 'value2'
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)


def test_json_format_empty_files():
    """Тестирует JSON формат для пустых файлов."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump({}, f1)
        file1 = f1.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump({}, f2)
        file2 = f2.name
    
    try:
        result = generate_diff(file1, file2, 'json')
        parsed_result = json.loads(result)
        assert parsed_result == []  # Для одинаковых пустых файлов - пустой список
    finally:
        import os
        os.unlink(file1)
        os.unlink(file2)