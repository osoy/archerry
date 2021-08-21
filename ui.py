from typing import Optional
from os import path
from getpass import getpass

def safe_input(prompt: str, default='') -> str:
    if prompt[-1] != ' ': prompt += ': '
    try: return input(prompt) or default
    except KeyboardInterrupt: exit(1)
    except EOFError:
        print()
        return default

def input_bool(prompt: str) -> bool:
    if prompt[-1] != ' ': prompt += '? '
    while True:
        val = safe_input(prompt)
        if not val: continue
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
        matches = [opt for opt in options if query.lower() in opt.lower()]
        if len(matches) == 1:
            print(f'> {matches[0]}')
            return matches[0]
        elif len(matches) == 0: print('No matches')
        elif query: print('Multiple matches')

def input_file(prompt: str) -> str:
    while True:
        val = safe_input(prompt)
        if not val: continue
        elif path.isfile(val): return val
        else: print(f"File '{val}' not found")

def input_secret(prompt: str) -> str:
    while True:
        secret = getpass(f'{prompt}: ')
        if not secret: continue
        secret_ensure = getpass(f'{prompt} again: ')
        if secret == secret_ensure: return secret
        else: print('Secrets do not match')
