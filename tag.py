def list_of(spec: dict, key: str) -> list[any]:
    if isinstance(spec, list):
        res = []
        for item in spec: res.extend(list_of(item, key))
        return res
    elif isinstance(spec, str): return spec.split()
    elif isinstance(spec, dict):
        if spec[key]: return list_of(spec[key], key)
        else: return [spec]
    else: return []
