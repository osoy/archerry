from itertools import chain

def list_of(spec: any, key: str) -> list[any]:
    if isinstance(spec, list):
        return [v for item in spec for v in list_of(item, key)]
    elif isinstance(spec, dict) and spec.get(key):
        return list_of(spec[key], key)
    else: return [spec]

def full_list_of(spec: any, key: str) -> list[any]:
    if isinstance(spec, list):
        return [v for item in spec for v in full_list_of(item, key)]
    elif isinstance(spec, dict):
        result = []
        if value := spec.get(key): result.append(value)
        result += full_list_of(list(spec.values()), key)
        return result
    else: return []
