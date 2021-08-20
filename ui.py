from typing import Optional
from os import path

def safe_input(prompt: str, default = '') -> str:
    try: return input(prompt + ': ') or default
    except KeyboardInterrupt: exit(1)
    except: return default

def input_int(prompt: str, default = 0) -> int:
    while True:
        try: return int(safe_input(prompt) or 0)
        except: pass

def input_natural(prompt: str, default = 0) -> int:
    while True:
        val = input_int(prompt, default)
        if val >= 0: return val

def input_choice(prompt: str, options: set[str]) -> str:
    while True:
        query = safe_input('%s (%s)' % (prompt, ', '.join(options)))
        matches = [opt for opt in options if query in opt]
        if len(matches) == 1: return matches[0]

def input_file(prompt: str) -> str:
    while True:
        val = safe_input(prompt)
        if not val: continue
        elif path.isfile(val): return val
        else: print(f"file '{val}' not found")
