from itertools import chain
import yaml
import tag
from installer import *
import templates

class Specification(dict):
    @classmethod
    def from_file(cls, name: str):
        with open(name, 'r') as file: return cls(yaml.safe_load(file))

    def installer(self) -> Installer:
        return (Installer.PACMAN, Installer.YAY) [self['yay'] == True]

    def pkg_list(self) -> list[str]:
        return list(chain(*map(
            lambda item : item.split(),
            tag.list_of(self, 'pkg'))))

    def pkg_script(self) -> str:
        return self.installer().script(self.pkg_list())

    def git_script(self) -> str:
        return '\n'.join(map(
            lambda entry : 'git clone %s %s' % (entry['repo'], entry['path']),
            tag.list_of(self, 'git')))

    def fs_script(self) -> str:
        return '\n'.join(map(
            lambda entry : templates.WRITE.substitute(
                path = entry['path'],
                content = entry['write']),
            tag.list_of(self, 'fs')))

    def custom_script(self) -> str:
        return '\n'.join(tag.list_of(self, 'cmd'))

    def script(self) -> str:
        return '\n\n\n'.join([
            self.pkg_script(),
            self.git_script(),
            self.fs_script(),
            self.custom_script(),
        ])
