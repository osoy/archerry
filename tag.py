from typing import Optional
from utils import flatten, overlap

def list_of(
    spec: any,
    key: str,
    tags: Optional[list[str]] = None,
    debounce = True,
) -> list[any]:
    if isinstance(spec, list):
        return flatten([list_of(item, key, tags, False) for item in spec])
    elif isinstance(spec, dict) and key in spec:
        if tags != None and 'tag' in spec:
            selectors = spec['tag']
            if isinstance(selectors, str): selectors = selectors.split()
            if not overlap(tags, selectors): return []
        return list_of(spec[key], key, tags, False)
    else: return ([spec], []) [debounce]

def full_list_of(spec: any, key: str, debounce = True) -> list[any]:
    if isinstance(spec, list):
        return flatten([full_list_of(item, key, debounce) for item in spec])
    elif isinstance(spec, dict) and (debounce or key in spec):
        return flatten([full_list_of(spec[k], key, k != key) for k in spec])
    else: return ([spec], []) [debounce]
