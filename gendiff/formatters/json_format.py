import json


def format_json(diff: list) -> str:
    """
    Форматирует diff в JSON формате.
    
    Args:
        diff: Внутреннее представление diff
    
    Returns:
        JSON строка с представлением diff
    """
    def process_node(node: dict) -> dict:
        """Обрабатывает узел для JSON сериализации."""
        result = {
            'key': node['key'],
            'type': node['type']
        }
        
        node_type = node['type']
        
        if node_type == 'nested':
            result['children'] = [
                process_node(child) for child in node['children']
            ]
        elif node_type == 'added':
            result['value'] = node['value']
        elif node_type == 'removed':
            result['value'] = node['value']
        elif node_type == 'changed':
            result['old_value'] = node['old_value']
            result['new_value'] = node['new_value']
        elif node_type == 'unchanged':
            result['value'] = node['value']
        
        return result
    
    # Преобразуем diff в структуру для JSON
    json_diff = [process_node(node) for node in diff]
    return json.dumps(json_diff, indent=2, ensure_ascii=False)