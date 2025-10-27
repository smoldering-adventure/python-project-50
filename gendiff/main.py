def generate_diff(first_file: str, second_file: str, output_format: str = 'plain') -> None:
    """
    Основная функция утилиты gendiff.
    На данном этапе просто выводит, что файлы были получены.
    """
    print(f"gendiff: Сравниваем файлы '{first_file}' и '{second_file}'")
    print(f"gendiff: Формат вывода: '{output_format}'")