from subprocess import run, PIPE, CompletedProcess
from math import log

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

def bash(cmd: str) -> CompletedProcess:
    return run(['bash', '-c', cmd], stdout=PIPE)

def bash_out(cmd: str) -> str:
    return bash(cmd).stdout.decode('utf-8')

def bash_lines(cmd: str) -> list[str]:
    return bash_out(cmd).strip().split('\n')

BIN_PREFIX = ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']

def prefix_bin(count: int) -> str:
    power = min(int(log(count, 1024)), len(BIN_PREFIX))
    if power == 0: return f'{count}B'
    prefix = BIN_PREFIX[power - 1]
    value = count / (1024 ** power)
    return f'{value:.1f}{prefix}B'
