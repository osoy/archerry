from itertools import chain

def list_of(spec: dict, key: str) -> list[any]:
    if isinstance(spec, list):
        return list(chain(*map(lambda item : list_of(item, key), spec)))
    elif isinstance(spec, dict) and spec.get(key):
        return list_of(spec[key], key)
    else: return [spec]
