import argparse
import sys

from gendiff.main import generate_diff  # type: ignore


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
        default='plain',
        help='set format of output'
    )

    args = parser.parse_args()

    # Вызываем основную функцию, передавая ей аргументы
    try:
        # Вызываем основную функцию, передавая ей аргументы
        result = generate_diff(args.first_file, args.second_file, args.format)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()