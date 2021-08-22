from subprocess import run, PIPE, DEVNULL

def repo_url(val: str) -> str:
    if '@' not in val and '://' not in val: val = f'https://{val}'
    return val

def base_dir(path: str) -> str:
    return '/'.join(path.split('/')[0:-1])

def write_script(content: str, path: str) -> str:
    prefix = ('', 'sudo ') [path[0] == '/']
    mkdir_script = f'{prefix}mkdir -p {base_dir(path)}'
    print_script = f"printf '{content}' | {prefix}tee {path} >/dev/null"
    return '\n'.join([mkdir_script, print_script])

def concat(entries: list[str], level = 1) -> str:
    sep = '\n'
    if level == 0: sep = ' \\\n\t'
    elif level == 2: sep = '\n\n\n'
    return sep.join([e.strip() for e in entries])

def bash_pipe(cmd: str) -> str:
    return run(
        ['bash', '-c', cmd],
        stdout=PIPE,
        stderr=DEVNULL,
    ).stdout.decode('utf-8')

def bash_lines(cmd: str) -> list[str]:
    return bash_pipe(cmd).strip().split('\n')
