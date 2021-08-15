import yaml
from installer import *

def pkg_list_of(spec: dict) -> list[str]:
    if isinstance(spec, list):
        res = []
        for pkg in spec:
            res.extend(pkg_list_of(pkg))
        return res
    elif isinstance(spec, str): return spec.split()
    elif isinstance(spec, dict): return pkg_list_of(spec['pkg'])
    else: return []

class Specification(dict):
    @classmethod
    def from_file(cls, name: str):
        with open(name, 'r') as file: return cls(yaml.safe_load(file))

    def installer(self) -> Installer:
        return (Installer.pacman, Installer.yay) [self['yay'] == True]

    def pkg_script(self) -> str:
        return self.installer().to_script(pkg_list_of(self))
