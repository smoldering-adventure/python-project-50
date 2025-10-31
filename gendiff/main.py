import json


def generate_diff(
    first_file: str, second_file: str, output_format: str = 'plain'
    ) -> str:
    """
    Основная функция утилиты gendiff.
    Читает два JSON-файла, парсит их и выводит информацию.
    """
    file1 = json.load(open(first_file))
    file2 = json.load(open(second_file))

    # Форматирование булевых значений
    def format_values(value):
        if isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return "null"
        else:
            return str(value)
        
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


