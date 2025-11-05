import json
import os
from typing import Any, Dict

import yaml


# --- Вспомогательная функция для форматирования значений ---
def format_values(value: Any) -> str:
    """
    Форматирует значения для вывода, преобразуя булевы в нижний регистр
    и None в 'null'.
    """
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return "null"
    else:
        return str(value)


def validate_file(filepath: str) -> None:
    """
    Проверяет существование и доступность файла.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    if not os.path.isfile(filepath):
        raise ValueError(f"Не является файлом: {filepath}")
    

def determine_file_format(filepath: str, file_format: str = None) -> str:
    """
    Определяет формат файла по расширению, если не указан явно.
    """
    if file_format is not None:
        return file_format
    
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()
    
    if extension == '.json':
        return 'json'
    elif extension in ('.yaml', '.yml'):
        return 'yaml'
    else:
        raise ValueError(
            f"Неподдерживаемый формат файла: {filepath}. "
            f"Поддерживаются JSON (.json) и YAML (.yaml, .yml)"
        )


def parse_json_file(filepath: str) -> Dict[str, Any]:
    """Парсит JSON файл."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON в файле {filepath}: {e}")


def parse_yaml_file(filepath: str) -> Dict[str, Any]:
    """Парсит YAML файл."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Некорректный YAML в файле {filepath}: {e}")
    

def read_file_content(filepath: str, source_format) -> Dict[str, Any]:
    """
    Читает файл и возвращает его содержимое в виде словаря.
    """
    validate_file(filepath)
    format_type = determine_file_format(filepath, source_format)
    
    if format_type == 'json':
        return parse_json_file(filepath)
    elif format_type == 'yaml':
        return parse_yaml_file(filepath)


def load_data(source: Any, source_format) -> Dict[str, Any]:
    """
    Загружает данные из источника: 
    либо парсит JSON из файла, либо берет словарь.
    """
    if isinstance(source, dict):
        return source 
    elif isinstance(source, str):
        return read_file_content(source, source_format) 
    else:
        raise TypeError(
            "Источник должен быть путем "
            "к файлу (str) или словарем (dict)"
        )


# --- Основная функция сравнения ---
def generate_diff(
    first_file: Any, second_file: Any, output_format: str = 'plain'
    ) -> str:
    """
    Основная функция утилиты gendiff.
    Читает два файла (JSON или YAML), парсит их и выводит информацию.
    """

    try:
        file_format = None if output_format == 'plain' else output_format

        file1 = load_data(first_file, file_format)
        file2 = load_data(second_file, file_format)
    except (FileNotFoundError, ValueError, RuntimeError, TypeError) as e:
        return f"Ошибка: {e}"
    
    # Проверяем что данные являются словарями
    if not isinstance(file1, dict) or not isinstance(file2, dict):
        return "Ошибка: Оба источника должны содержать объекты"
        
    all_key = sorted(set(file1.keys()) | set(file2.keys()))
    diff_lines = []

    for key in all_key:
        value1 = file1.get(key)
        value2 = file2.get(key)

        if key in file1 and key in file2:
            if value1 == value2:
                diff_lines.append(f"    {key}: {format_values(value1)}")
            else:
                diff_lines.append(f"  - {key}: {format_values(value1)}")
                diff_lines.append(f"  + {key}: {format_values(value2)}")
        elif key in file1:
            diff_lines.append(f"  - {key}: {format_values(value1)}")
        else:
            diff_lines.append(f"  + {key}: {format_values(value2)}")
    
    return "{\n" + '\n'.join(diff_lines) + "\n}"


