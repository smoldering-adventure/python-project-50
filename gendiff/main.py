from typing import Any, Dict

from gendiff.formatters import format_diff
from gendiff.scripts.diff_builder import build_diff
from gendiff.scripts.parsers import read_file_content


def load_data(source: Any) -> Dict[str, Any]:
    """
    Загружает данные из источника: 
    либо парсит JSON из файла, либо берет словарь.
    """
    if isinstance(source, dict):
        return source 
    elif isinstance(source, str):
        return read_file_content(source) 
    else:
        raise TypeError(
            "Источник должен быть путем "
            "к файлу (str) или словарем (dict)"
        )


# --- Основная функция сравнения ---
def generate_diff(
    first_file: Any, second_file: Any, format_name: str = 'stylish'
    ) -> str:
    """
    Основная функция утилиты gendiff.
    Читает два файла (JSON или YAML), парсит их и выводит информацию.
    """

    try:
        file1 = load_data(first_file)
        file2 = load_data(second_file)
    except (FileNotFoundError, ValueError, RuntimeError, TypeError) as e:
        return f"Ошибка: {e}"
    
    # Проверяем что данные являются словарями
    if not isinstance(file1, dict) or not isinstance(file2, dict):
        return "Ошибка: Оба источника должны содержать объекты"
    
    if format_name not in ['plain', 'stylish']:
        return f"Ошибка: Не поддерживаемый формат {format_name}"
    
    diff = build_diff(file1, file2)
    
    return format_diff(diff, format_name)


