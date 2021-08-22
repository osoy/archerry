from itertools import chain
from pathlib import Path
import yaml
import tag
from installer import Installer
from utils import repo_url, base_dir, write_script, concat
import templates

class Specification(dict):
    @classmethod
    def from_file(cls, name: str):
        try:
            with open(name, 'r') as file: return cls(yaml.safe_load(file))
        except:
            print(f"could not read '{name}'")
            exit(4)

    def installer(self) -> Installer:
        return (Installer.PACMAN, Installer.YAY) [self.get('yay') == True]

    def pkg_list(self) -> list[str]:
        return list(chain(*map(
            lambda item : item.split(),
            tag.list_of(self, 'pkg'))))

    def pkg_script(self) -> str:
        return self.installer().script(self.pkg_list())

    def git_script(self) -> str:
        return concat(map(
            lambda entry : 'git clone %s %s' % (
                repo_url(entry['repo']),
                entry.get('path') or ''),
            tag.list_of(self, 'git')))

    def writes(self) -> list[dict]:
        return tag.list_of(self, 'fs')

    def fs_script(self) -> str:
        return concat(map(
            lambda entry : write_script(entry['write'], entry['path']),
            self.writes()))

    def custom_script(self) -> str:
        return concat(tag.list_of(self, 'cmd'))

    def script(self) -> str:
        return concat([
            self.pkg_script(),
            self.git_script(),
            self.fs_script(),
            self.custom_script(),
        ], 2)

    def check_pkg(self):
        self.installer().check(self.pkg_list())

    def check_fs(self):
        missing_count = 0
        diff_count = 0
        entries = self.writes()
        for entry in entries:
            path = entry['path']
            if path[0:2] == '~/': path = str(Path.home()) + path[1:]
            try:
                with open(path, 'r') as file:
                    content = file.read()
                    if content.strip() != entry['write'].strip():
                        print('Diff: %s' % path)
                        diff_count += 1
            except:
                print('Missing: %s' % path)
                missing_count += 1
        print('Total %i, Missing %i, Diff %i' % \
            (len(entries), missing_count, diff_count))

    def check(self) -> str:
        print('Checking fs...')
        self.check_fs()
        print()
        print('Checking pkg...')
        self.check_pkg()
        print()
