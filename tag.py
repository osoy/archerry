from itertools import chain

def list_of(spec: any, key: str, debounce = True) -> list[any]:
    if isinstance(spec, list):
        return [v for item in spec for v in list_of(item, key, False)]
    elif isinstance(spec, dict) and spec.get(key):
        return list_of(spec[key], key, False)
    else: return ([spec], []) [debounce]

def full_list_of(spec: any, key: str, debounce = True) -> list[any]:
    if isinstance(spec, list):
        return [v for item in spec for v in full_list_of(item, key, debounce)]
    elif isinstance(spec, dict) and (debounce or spec.get(key)):
        return [v for k in spec for v in full_list_of(spec[k], key, k != key)]
    else: return ([spec], []) [debounce]
