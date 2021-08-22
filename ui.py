from typing import Optional, TypeVar
from math import log
from getpass import getpass

T = TypeVar('T')

def safe_input(prompt: str, default='') -> str:
    if prompt[-1] != ' ': prompt += ': '
    try: return input(prompt) or default
    except KeyboardInterrupt: exit(1)
    except EOFError:
        print()
        return default

def input_bool(prompt: str, default=None) -> bool:
    if prompt[-1] != ' ': prompt += '? '
    while True:
        val = safe_input(prompt)
        if not val:
            if default != None: return default
            else continue
        if val.upper() in ['Y', 'YES']: return True
        if val.upper() in ['N', 'NO']: return False

def input_word(prompt: str, default=0) -> int:
    while True:
        val = safe_input(prompt, default)
        if not val: continue
        return val.strip().replace(' ', '_')

def input_int(prompt: str, default=0) -> int:
    while True:
        val = safe_input(prompt)
        try: return int(val or default)
        except: pass

def input_natural(prompt: str, default=0) -> int:
    while True:
        val = input_int(prompt, default)
        if val >= 0: return val
        else: print('Must be 0 or greater')

def input_choice(prompt: str, options: set[str]) -> str:
    while True:
        query = safe_input(prompt)
        if query in options: return query
        matches = [opt for opt in options if query.upper() in opt.upper()]
        if len(matches) == 1:
            print(f'> {matches[0]}')
            return matches[0]
        elif len(matches) == 0: print('No matches')
        elif query: print('Multiple matches')

def input_index(prompt: str, options: list[T]) -> T:
    while True:
        index = input_natural(prompt, None)
        if index == None or index >= len(options): continue
        return options[index]

def input_secret(prompt: str) -> str:
    while True:
        secret = getpass(f'{prompt}: ')
        if not secret: continue
        secret_ensure = getpass(f'{prompt} again: ')
        if secret == secret_ensure: return secret
        else: print('Secrets do not match')

def table(rows: list[list[str]], sep='  ') -> str:
    if len(rows) < 1: return ''
    widths = {}
    for row in rows:
        for i, v in enumerate(row): widths[i] = max(widths.get(i) or 0, len(v))
    lines = []
    for row in rows:
        items = [v + ' ' * (widths.get(i) - len(v)) for i, v in enumerate(row)]
        lines.append(sep.join(items))
    return '\n'.join(lines)

BIN_PREFIX = ['Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']

def prefix_bin(count: int) -> str:
    power = min(int(log(count, 1024)), len(BIN_PREFIX))
    if power == 0: return f'{count}B'
    prefix = BIN_PREFIX[power - 1]
    value = count / (1024 ** power)
    return f'{value:.1f}{prefix}B'
