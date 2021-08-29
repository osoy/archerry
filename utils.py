from typing import Union
from os.path import realpath, isdir
from subprocess import run, PIPE, DEVNULL

def repo_url(val: str) -> str:
    if '@' not in val and '://' not in val: val = f'https://{val}'
    if val[-4:] != '.git': val += '.git'
    return val

def base_dir(path: str) -> str:
    if not len(path): return '.'
    if len(path) > 1 and path[-1] == '/': path = path[0:-1]
    result = '/'.join(path.split('/')[0:-1])
    if result: return result
    else:
        if path[0] == '/': return '/'
        else: return '.'

def rel_path(path: str) -> str:
    if path and path[0] != '/': path = '/' + path
    return base_dir(realpath(__file__)) + path

def concat(entries: list[str], level = 1) -> str:
    sep = '\n'
    if level == 0: sep = ' \\\n\t'
    elif level == 2: sep = '\n\n\n'
    return sep.join([e.strip() for e in entries])

def search(query: str, options: set[str]) -> Union[str, list[str]]:
    if query in options: return query
    return [opt for opt in options if query.upper() in opt.upper()]

def flatten(arr: list[any]) -> list[any]:
    result = []
    for elem in arr:
        if isinstance(elem, list): result += flatten(elem)
        else: result.append(elem)
    return result

def overlap(left: list[any], right: list[any]) -> bool:
    for item in left:
        if item in right: return True
    return False

def bash_pipe(cmd: str) -> str:
    return run(
        ['bash', '-c', cmd],
        stdout=PIPE,
        stderr=DEVNULL,
    ).stdout.decode('utf-8')

def bash_lines(cmd: str) -> list[str]:
    return bash_pipe(cmd).strip().split('\n')

def write_script(content: str, path: str) -> str:
    prefix = ('', 'sudo ') [path[0] == '/']
    mkdir_script = f'{prefix}mkdir -p {base_dir(path)}'
    print_script = f"printf '{content}' | {prefix}tee {path} >/dev/null"
    return concat([mkdir_script, print_script])

def write_file(path: str, content: str, out = True):
    directory = base_dir(path)
    if not isdir(directory): run(['mkdir', '-p', directory])
    with open(path, 'w') as file: file.write(content)
    if out: print(f'Wrote {len(content)} characters to {path}')
