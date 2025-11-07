from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish


def format_diff(diff: list, format_name: str) -> str:
    """
    Форматирует diff в указанном формате.
    
    Args:
        diff: Внутреннее представление diff
        format_name: Название формата ('stylish', 'plain')
    
    Returns:
        Отформатированная строка
    """
    if format_name == 'stylish':
        return format_stylish(diff)
    elif format_name == 'plain':
        return format_plain(diff)
    else:
        raise ValueError(f"Unsupported format: {format_name}")