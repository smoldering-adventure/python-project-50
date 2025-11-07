from typing import Any, Dict

from gendiff.scripts.parsers import read_file_content


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
    first_file: Any, second_file: Any, output_format: str = 'plain'
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
    
    if output_format != 'plain':
        return f"Ошибка: Неподдерживаемый формат вывода: {output_format}"
        
    all_keys = sorted(set(file1.keys()) | set(file2.keys()))
    diff_lines = []

    for key in all_keys:
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


