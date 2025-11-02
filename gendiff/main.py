import json
import os

# --- Вспомогательная функция для форматирования значений ---
def format_values(value):
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

# --- Вспомогательная функция для чтения файла с проверками ---
def read_file_content(filepath: str):
    """
    Читает JSON-файл, парсит его и возвращает содержимое.
    Обрабатывает ошибки отсутствия файла и некорректного JSON.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        raise ValueError(f"Некорректный JSON в файле: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {filepath}: {e}")


# --- Основная функция сравнения ---
def generate_diff(
    first_file: str, second_file: str, output_format: str = 'plain'
    ) -> str:
    """
    Основная функция утилиты gendiff.
    Читает два JSON-файла, парсит их и выводит информацию.
    """
    try:
        file1 = read_file_content(first_file)
        file2 = read_file_content(second_file)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        return f"Ошибка: {e}"
        
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


