import argparse
from gendiff.main import generate_diff # type: ignore


def main():
    """
    Главная точка входа для скрипта gendiff.
    Настраивает argparse и вызывает основную функцию.
    """
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Позиционные аргументы
    parser.add_argument('first_file')
    parser.add_argument('second_file')

    # Опциональный аргумент --format
    parser.add_argument(
        '-f', '--format',
        metavar='FORMAT',
        help='set format of output'
        # Можно добавить choices=['plain', 'json'], если нужно ограничить форматы
    )

    args = parser.parse_args()

    # Вызываем основную функцию, передавая ей аргументы
    generate_diff(args.first_file, args.second_file, args.format)


if __name__ == "__main__":
    main()