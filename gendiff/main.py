import json

def generate_diff(first_file: str, second_file: str, output_format: str = 'plain') -> None:
    """
    Основная функция утилиты gendiff.
    Читает два JSON-файла, парсит их и выводит информацию.
    """
    fale1 = json.load(open(first_file))
    fale2 = json.load(open(second_file))

    print(f"gendiff: Данные из {first_file}: {fale1}")
    print(f"gendiff: Данные из {second_file}: {fale2}")

    print(f"gendiff: Формат вывода: '{output_format}'")