from typing import Any, Dict


def format_value(value: Any, depth: int) -> str:
    """Форматирует значение для вывода в stylish формате."""
    if isinstance(value, dict):
        return format_dict(value, depth + 1)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)


def format_dict(data: Dict, depth: int) -> str:
    """Форматирует словарь для вывода в stylish формате."""
    if not data:
        return '{}'
    
    indent = '    ' * depth
    lines = []
    
    for key, value in sorted(data.items()):
        formatted_value = format_value(value, depth)
        lines.append(f"{indent}    {key}: {formatted_value}")
    
    result = '\n'.join(lines)
    return f"{{\n{result}\n{indent[:-4]}}}"


def format_stylish(diff: list, depth: int = 0) -> str:
    """
    Форматирует diff в stylish формате.
    
    Args:
        diff: Внутреннее представление diff
        depth: Текущая глубина вложенности
    
    Returns:
        Отформатированная строка
    """
    indent = '    ' * depth
    lines = []
    
    for node in diff:
        key = node['key']
        node_type = node['type']
        
        if node_type == 'nested':
            formatted_children = format_stylish(node['children'], depth + 1)
            lines.append(f"{indent}    {key}: {formatted_children}")
        elif node_type == 'added':
            value = format_value(node['value'], depth)
            lines.append(f"{indent}  + {key}: {value}")
        elif node_type == 'removed':
            value = format_value(node['value'], depth)
            lines.append(f"{indent}  - {key}: {value}")
        elif node_type == 'changed':
            old_value = format_value(node['old_value'], depth)
            new_value = format_value(node['new_value'], depth)
            lines.append(f"{indent}  - {key}: {old_value}")
            lines.append(f"{indent}  + {key}: {new_value}")
        elif node_type == 'unchanged':
            value = format_value(node['value'], depth)
            lines.append(f"{indent}    {key}: {value}")
    
    if depth == 0:
        return f"{{\n{chr(10).join(lines)}\n}}"
    else:
        result = '\n'.join(lines)
        return f"{{\n{result}\n{indent}}}"