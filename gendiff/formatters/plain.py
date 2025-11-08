from typing import Any


def format_value(value: Any) -> str:
    """Форматирует значение для вывода."""
    if isinstance(value, dict):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)


def format_plain(diff: list, path: str = '') -> str:
    """
    Форматирует diff в plain формате.
    
    Args:
        diff: Внутреннее представление diff
        depth: Текущая глубина вложенности
    
    Returns:
        Отформатированная строка
    """
    lines = []
    
    for node in diff:
        key = node['key']
        # Формируем полный путь к свойству
        current_path = f"{path}.{key}" if path else key
        node_type = node['type']
        
        if node_type == 'nested':
            # Рекурсивно обрабатываем вложенные узлы
            nested_lines = format_plain(node['children'], current_path)
            if nested_lines:
                lines.append(nested_lines)
        elif node_type == 'added':
            value = format_value(node['value'])
            lines.append(f"Property '{current_path}' was added with value: {value}")
        elif node_type == 'removed':
            lines.append(f"Property '{current_path}' was removed")
        elif node_type == 'changed':
            old_value = format_value(node['old_value'])
            new_value = format_value(node['new_value'])
            lines.append(
                f"Property '{current_path}' was updated. "
                f"From {old_value} to {new_value}"
            )
        # unchanged узлы игнорируем в plain формате
    
    return '\n'.join(line for line in lines if line)