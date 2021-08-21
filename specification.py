from itertools import chain
import yaml
import tag
from installer import Installer
from ui import input_file
from utils import repo_url, base_dir, write_script, cat
import templates

class Specification(dict):
    @classmethod
    def from_file(cls, name: str):
        with open(name, 'r') as file: return cls(yaml.safe_load(file))

    @classmethod
    def from_input(cls):
        return Specification.from_file(input_file('config file'))

    def installer(self) -> Installer:
        return (Installer.PACMAN, Installer.YAY) [self.get('yay') == True]

    def pkg_list(self) -> list[str]:
        return list(chain(*map(
            lambda item : item.split(),
            tag.list_of(self, 'pkg'))))

    def pkg_script(self) -> str:
        return self.installer().script(self.pkg_list())

    def git_script(self) -> str:
        return cat(map(
            lambda entry : 'git clone %s %s' % (
                repo_url(entry['repo']),
                entry.get('path') or ''),
            tag.list_of(self, 'git')))

    def fs_script(self) -> str:
        return cat(map(
            lambda entry : write_script(entry['write'], entry['path']),
            tag.list_of(self, 'fs')))

    def custom_script(self) -> str:
        return cat(tag.list_of(self, 'cmd'))

    def script(self) -> str:
        return cat([
            self.pkg_script(),
            self.git_script(),
            self.fs_script(),
            self.custom_script(),
        ], 2)
