from typing import Any, Dict, List


def build_diff(data1: Dict[str, Any], data2: Dict[str, Any]) -> List[Dict]:
    """
    Строит внутреннее представление diff между двумя словарями.
    
    Возвращает список узлов, где каждый узел имеет:
    - key: ключ
    - type: 'added', 'removed', 'unchanged', 'changed', 'nested'
    - value: значение (для added, removed, unchanged)
    - old_value: старое значение (для changed)
    - new_value: новое значение (для changed)
    - children: список дочерних узлов (для nested)
    """
    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff = []

    for key in all_keys:
        value1 = data1.get(key)
        value2 = data2.get(key)

        if key not in data2:
            diff.append({
                'key': key,
                'type': 'removed',
                'value': value1
            })
        elif key not in data1:
            diff.append({
                'key': key,
                'type': 'added', 
                'value': value2
            })
        elif value1 == value2:
            diff.append({
                'key': key,
                'type': 'unchanged',
                'value': value1
            })
        elif isinstance(value1, dict) and isinstance(value2, dict):
            # Оба значения - словари, рекурсивно строим diff для них
            diff.append({
                'key': key,
                'type': 'nested',
                'children': build_diff(value1, value2)
            })
        else:
            # Значения разные и не оба словари
            diff.append({
                'key': key,
                'type': 'changed',
                'old_value': value1,
                'new_value': value2
            })
    
    return diff