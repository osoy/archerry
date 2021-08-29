from typing import Optional
from pathlib import Path
import yaml

import tag
from preferences import Preferences
from installer import Installer
from utils import repo_url, base_dir, write_script, concat, flatten
from ui import input_multichoice

class Specification(dict):
    tags: Optional[list[str]] = None

    @classmethod
    def from_file(cls, name: str):
        try:
            with open(name, 'r') as file: return cls(yaml.safe_load(file))
        except:
            print(f"could not read '{name}'")
            exit(4)

    def input_tags(self):
        tag_list = self.tag_list()
        print('Available tags: %s' % ' '.join(tag_list))
        self.tags = input_multichoice('Select tags', tag_list)

    def installer(self) -> Installer:
        return (Installer.PACMAN, Installer.YAY) [self.get('yay')]

    def tag_list(self) -> list[str]:
        return sorted(list(set(tag.full_list_of(self, 'tag'))))

    def pkg_list(self) -> list[str]:
        return flatten(
            [item.split() for item in tag.list_of(self, 'pkg', self.tags)])

    def pkg_script(self) -> str:
        return self.installer().script(self.pkg_list())

    def git_script(self) -> str:
        return concat(map(
            lambda entry : 'git clone %s %s' % \
                (repo_url(entry['repo']), entry.get('path') or ''),
            tag.list_of(self, 'git', self.tags)))

    def writes(self) -> list[dict]:
        return tag.list_of(self, 'fs', self.tags)

    def fs_script(self) -> str:
        return concat(
            [write_script(e['write'], e['path']) for e in self.writes()])

    def custom_script(self) -> str:
        return concat(tag.list_of(self, 'cmd', self.tags))

    def script(self) -> str:
        return concat([
            self.pkg_script(),
            self.git_script(),
            self.fs_script(),
            self.custom_script(),
        ], 2)

    def check_pkg(self) -> int:
        return self.installer().check(self.pkg_list())

    def check_fs(self) -> int:
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
                        print('Different: %s' % path)
                        diff_count += 1
            except:
                print('Missing: %s' % path)
                missing_count += 1
        print('Total %i, Missing %i, Different %i' % \
            (len(entries), missing_count, diff_count))
        return missing_count + diff_count

    def check(self) -> int:
        errors = 0
        print('Checking fs...')
        errors += self.check_fs()
        print()
        print('Checking pkg...')
        errors += self.check_pkg()
        print()
        return errors
