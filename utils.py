def repo_url(val: str) -> str:
    if '@' not in val and '://' not in val: val = f'https://{val}'
    return val

def base_dir(path: str) -> str:
    return '/'.join(path.split('/')[0:-1])

def write_script(content: str, path: str) -> str:
    prefix = ('', 'sudo ') [path[0] == '/']
    mkdir_script = prefix + 'mkdir -p ' + base_dir(path)
    print_script = prefix + f"printf '{content}' > {path}"
    return '\n'.join([mkdir_script, print_script])

def cat(entries: list[str], level = 1) -> str:
    sep = '\n'
    if level == 0: sep = ' \\\n\t'
    elif level == 2: sep = '\n\n\n'
    return sep.join(map(lambda e : e.strip(), entries))
