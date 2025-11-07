import json
import os
from typing import Any, Dict

import yaml  # type: ignore


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