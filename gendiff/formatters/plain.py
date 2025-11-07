from typing import Any


def format_value(value: Any) -> str:
    """Форматирует значение для вывода."""
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)


def format_plain(diff: list, depth: int = 0) -> str:
    """
    Форматирует diff в plain формате (простое дерево с +-).
    
    Args:
        diff: Внутреннее представление diff
        depth: Текущая глубина вложенности
    
    Returns:
        Отформатированная строка
    """
    lines = []
    indent = '  ' * depth
    
    for node in diff:
        key = node['key']
        node_type = node['type']
        
        if node_type == 'nested':
            # Для вложенных узлов
            lines.append(f"  {indent}  {key}: {{")
            children = format_plain(node['children'], depth + 1)
            lines.append(children)
            lines.append(f"  {indent}  }}")
        elif node_type == 'added':
            value = format_value(node['value'])
            lines.append(f"  {indent}+ {key}: {value}")
        elif node_type == 'removed':
            value = format_value(node['value'])
            lines.append(f"  {indent}- {key}: {value}")
        elif node_type == 'changed':
            old_value = format_value(node['old_value'])
            new_value = format_value(node['new_value'])
            lines.append(f"  {indent}- {key}: {old_value}")
            lines.append(f"  {indent}+ {key}: {new_value}")
        elif node_type == 'unchanged':
            value = format_value(node['value'])
            lines.append(f"  {indent}  {key}: {value}")
    
    result = '\n'.join(lines)
    
    if depth == 0:
        return f"{{\n{result}\n}}"
    else:
        return result