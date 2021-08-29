from utils import flatten

def list_of(spec: any, key: str, debounce = True) -> list[any]:
    if isinstance(spec, list):
        return flatten([list_of(item, key, False) for item in spec])
    elif isinstance(spec, dict) and spec.get(key):
        return list_of(spec[key], key, False)
    else: return ([spec], []) [debounce]

def full_list_of(spec: any, key: str, debounce = True) -> list[any]:
    if isinstance(spec, list):
        return flatten([full_list_of(item, key, debounce) for item in spec])
    elif isinstance(spec, dict) and (debounce or spec.get(key)):
        return flatten([full_list_of(spec[k], key, k != key) for k in spec])
    else: return ([spec], []) [debounce]
