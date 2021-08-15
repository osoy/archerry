import yaml
import tag
from installer import *

class Specification(dict):
    @classmethod
    def from_file(cls, name: str):
        with open(name, 'r') as file: return cls(yaml.safe_load(file))

    def installer(self) -> Installer:
        return (Installer.pacman, Installer.yay) [self['yay'] == True]

    def pkg_script(self) -> str:
        return self.installer().to_script(tag.list_of(self, 'pkg'))
