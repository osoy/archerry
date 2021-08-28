from unittest import main, TestCase
from tag import list_of, full_list_of

class TestTag(TestCase):
    def test_list_of_strs(self):
        self.assertEqual(list_of({}, 'key'), [])
        self.assertEqual(list_of({ 'top': { 'key': 'smth' } }, 'key'), [])
        self.assertEqual(list_of({
            'pkg': ['tree tmux', 'nvim']
        }, 'pkg'), ['tree tmux', 'nvim'])
        self.assertEqual(list_of({
            'pkg': [
                'tree tmux',
                'nvim',
                {
                    'tag': 'gui',
                    'pkg': ['xorg', { 'tag': 'web', 'pkg': 'firefox' }]
                }
            ]
        }, 'pkg'), ['tree tmux', 'nvim', 'xorg', 'firefox'])

    def test_list_of_dicts(self):
        self.assertEqual(list_of({
            'git': [{ 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' }]
        }, 'git'), [{ 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' }])
        self.assertEqual(list_of({
            'git': [
                { 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' },
                {
                    'tag': 'config',
                    'git': [{ 'repo': 'gitlab.com/user/cfg', 'path': 'cfg' }]
                }
            ]
        }, 'git'), [
            { 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' },
            { 'repo': 'gitlab.com/user/cfg', 'path': 'cfg' }
        ])

    def test_full_list_of_strings(self):
        self.assertEqual(full_list_of({ 'tag': 'smth' }, 'tag'), ['smth'])
        self.assertEqual(full_list_of({
            'pkg': [
                'tree tmux',
                'nvim',
                {
                    'tag': 'gui',
                    'pkg': ['xorg', { 'tag': 'web', 'pkg': 'firefox' }]
                }
            ],
            'git': [
                { 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' },
                {
                    'tag': ['config', 'cfg'],
                    'git': [{ 'repo': 'gitlab.com/user/cfg', 'path': 'cfg' }]
                }
            ]
        }, 'tag'), ['gui', 'web', 'config', 'cfg'])

    def test_full_list_of_dictionaries(self):
        self.assertEqual(full_list_of({
            'pkg': [
                'tree tmux',
                'nvim',
                { 'tag': { 'gui': 1 }, 'pkg': { 'tag': { 'web': 1 } } }
            ],
            'git': [
                { 'repo': 'gitlab.com/osoy/osoy', 'path': 'osoy' },
                {
                    'tag': [{ 'config': 1 }, { 'cfg': 1 }],
                    'git': [{ 'repo': 'gitlab.com/user/cfg', 'path': 'cfg' }]
                }
            ]
        }, 'tag'), [{ 'gui': 1 }, { 'web': 1 }, { 'config': 1 }, { 'cfg': 1 }])
