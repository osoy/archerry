from unittest import TestCase
from tag import *

OSOY_CLONE = { 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' }
CFG_CLONE = { 'repo': 'gitlab.com/user/cfg', 'path': 'cfg' }
DWM_CLONE = { 'repo': 'gitlab.com/user/dwm', 'path': 'dwm' }

SPEC = {
    'pkg': [
        'tree tmux',
        'nvim',
        {
            'tag': 'gui',
            'pkg': ['xorg', { 'tag': 'web firefox', 'pkg': 'firefox' }]
        }
    ],
    'git': [
        OSOY_CLONE,
        {
            'tag': ['config', 'cfg'],
            'git': [CFG_CLONE, { 'tag': 'dwm', 'git': DWM_CLONE }]
        }
    ]
}

class TestTag(TestCase):
    def test_list_of_strs(self):
        self.assertEqual(list_of({}, 'key'), [])
        self.assertEqual(list_of({ 'top': { 'key': 'smth' } }, 'key'), [])
        self.assertEqual(
            list_of({ 'pkg': ['tree tmux', 'nvim'] }, 'pkg'),
            ['tree tmux', 'nvim'])
        self.assertEqual(
            list_of(SPEC, 'pkg'),
            ['tree tmux', 'nvim', 'xorg', 'firefox'])
        self.assertEqual(list_of(SPEC, 'pkg', []), ['tree tmux', 'nvim'])
        self.assertEqual(list_of(SPEC, 'pkg', ['web']), ['tree tmux', 'nvim'])
        self.assertEqual(
            list_of(SPEC, 'pkg', ['gui']),
            ['tree tmux', 'nvim', 'xorg'])
        self.assertEqual(
            list_of(SPEC, 'pkg', ['gui', 'web']),
            ['tree tmux', 'nvim', 'xorg', 'firefox'])
        self.assertEqual(
            list_of(SPEC, 'pkg', ['gui', 'firefox']),
            ['tree tmux', 'nvim', 'xorg', 'firefox'])
        self.assertEqual(
            list_of(SPEC, 'pkg', ['gui', 'web', 'firefox']),
            ['tree tmux', 'nvim', 'xorg', 'firefox'])

    def test_list_of_dicts(self):
        self.assertEqual(list_of({
            'git': [OSOY_CLONE]
        }, 'git'), [OSOY_CLONE])
        self.assertEqual(
            list_of(SPEC, 'git'),
            [OSOY_CLONE, CFG_CLONE, DWM_CLONE])
        self.assertEqual(list_of(SPEC, 'git', []), [OSOY_CLONE])
        self.assertEqual(
            list_of(SPEC, 'git', ['cfg']),
            [OSOY_CLONE, CFG_CLONE])
        self.assertEqual(
            list_of(SPEC, 'git', ['config']),
            [OSOY_CLONE, CFG_CLONE])
        self.assertEqual(list_of(SPEC, 'git', ['dwm']), [OSOY_CLONE])
        self.assertEqual(
            list_of(SPEC, 'git', ['cfg', 'dwm']),
            [OSOY_CLONE, CFG_CLONE, DWM_CLONE])

    def test_full_list_of_strings(self):
        self.assertEqual(full_list_of({ 'tag': 'smth' }, 'tag'), ['smth'])
        self.assertEqual(
            full_list_of(SPEC, 'tag'),
            ['gui', 'web firefox', 'config', 'cfg', 'dwm'])

    def test_full_list_of_dictionaries(self):
        self.assertEqual(full_list_of({
            'pkg': [
                'tree tmux',
                'nvim',
                { 'tag': { 'gui': 1 }, 'pkg': { 'tag': { 'web': 1 } } }
            ],
            'git': [
                OSOY_CLONE,
                {
                    'tag': [{ 'config': 1 }, { 'cfg': 1 }],
                    'git': [CFG_CLONE]
                }
            ]
        }, 'tag'), [{ 'gui': 1 }, { 'web': 1 }, { 'config': 1 }, { 'cfg': 1 }])
