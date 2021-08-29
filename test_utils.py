from unittest import TestCase
from utils import *

class Test(TestCase):
    def test_repo_url(self):
        self.assertEqual(
            repo_url('https://gitlab.com/osoy/osoy.git'),
            'https://gitlab.com/osoy/osoy.git')
        self.assertEqual(
            repo_url('gitlab.com/osoy/osoy'),
            'https://gitlab.com/osoy/osoy.git')
        self.assertEqual(
            repo_url('git@gitlab.com/osoy/osoy'),
            'git@gitlab.com/osoy/osoy.git')

    def test_base_dir(self):
        self.assertEqual(base_dir(''), '.')
        self.assertEqual(base_dir('/'), '/')
        self.assertEqual(base_dir('/etc'), '/')
        self.assertEqual(base_dir('/home/user'), '/home')
        self.assertEqual(base_dir('~/.ssh'), '~')
        self.assertEqual(base_dir('dist'), '.')
        self.assertEqual(base_dir('dist/user.bash'), 'dist')

    def test_concat(self):
        self.assertEqual(concat(['a', 'b', 'c']), 'a\nb\nc')
        self.assertEqual(concat(['a', 'b', 'c'], 1), 'a\nb\nc')
        self.assertEqual(concat(['a', 'b', 'c'], 2), 'a\n\n\nb\n\n\nc')
        self.assertEqual(concat(['a', 'b', 'c'], 0), 'a \\\n\tb \\\n\tc')

    def test_search(self):
        self.assertEqual(search('', []), [])
        self.assertEqual(search('', ['a', 'b']), ['a', 'b'])
        self.assertEqual(search('a', []), [])
        self.assertEqual(search('a', ['a', 'A']), 'a')
        self.assertEqual(search('a', ['A', 'aa']), ['A', 'aa'])
        self.assertEqual(search('A', ['A', 'aa']), 'A')
        self.assertEqual(search('A', ['Aa', 'aa']), ['Aa', 'aa'])
        self.assertEqual(search('Aa', ['Aa', 'aa']), 'Aa')

    def test_overlap(self):
        self.assertEqual(overlap([], []), [])
        self.assertEqual(overlap([1], []), [])
        self.assertEqual(overlap([], [1]), [])
        self.assertEqual(overlap([2], [1]), [])
        self.assertEqual(overlap([7, 4], [1, 2, 3]), [])
        self.assertEqual(overlap([1, 2], [1]), [1])
        self.assertEqual(overlap([1], [1, 2]), [1])
        self.assertEqual(overlap([3, 1, 4], [1, 2, 3]), [3, 1])

    def test_exclude(self):
        self.assertEqual(exclude([], []), [])
        self.assertEqual(exclude([1], []), [1])
        self.assertEqual(exclude([], [1]), [])
        self.assertEqual(exclude([2], [1]), [2])
        self.assertEqual(exclude([7, 4], [1, 2, 3]), [7, 4])
        self.assertEqual(exclude([1, 2], [1]), [2])
        self.assertEqual(exclude([1], [1, 2]), [])
        self.assertEqual(exclude([3, 1, 4], [1, 2, 3]), [4])

    def test_bash_pipe(self):
        self.assertEqual(bash_pipe("printf '%i\n' $((1+2))"), '3\n')

    def test_bash_lines(self):
        self.assertEqual(bash_lines("printf '1\n2\n3'"), ['1', '2', '3'])
        self.assertEqual(bash_lines("printf '1\n2\n3\n'"), ['1', '2', '3'])
        self.assertEqual(bash_lines("printf '\n1\n\n3\n\n'"), ['1', '', '3'])

    def test_write_script(self):
        self.assertEqual(
            write_script('hello', 'h.txt'),
            "mkdir -p .\nprintf 'hello' | tee h.txt >/dev/null")
        self.assertEqual(
            write_script('hello', '~/docs/h.txt'),
            "mkdir -p ~/docs\nprintf 'hello' | tee ~/docs/h.txt >/dev/null")
        self.assertEqual(
            write_script('hello', '/docs/h.txt'),
            "sudo mkdir -p /docs\nprintf 'hello' | "
            + "sudo tee /docs/h.txt >/dev/null")

    def test_flatten(self):
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[[], []], []]), [])
        self.assertEqual(flatten([1]), [1])
        self.assertEqual(flatten([1, [], [], 2]), [1, 2])
        self.assertEqual(flatten([[[1]], [[], [3]]]), [1, 3])
