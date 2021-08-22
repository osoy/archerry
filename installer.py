from enum import Enum
from subprocess import run, DEVNULL
from utils import cat
import templates

INSTALLER_FLAGS = ''

class Installer(str, Enum):
    PACMAN = 'sudo pacman'
    YAY = 'yay'

    def with_flags(self) -> str:
        return f'{self} -Syu --needed --noconfirm'

    def script(self, pkg_list: list[str]) -> str:
        call = cat([self.with_flags()] + pkg_list, 0)
        if self == Installer.YAY: call = cat([templates.INSTALL_YAY, call], 2)
        return call

    def check(self, pkg_list: list[str]):
        if self == Installer.YAY: pkg_list.append('yay')
        missing_count = 0
        for pkg in pkg_list:
            proc = run(['pacman', '-Q', pkg], stdout=DEVNULL, stderr=DEVNULL)
            if proc.returncode < 0: exit(1)
            elif proc.returncode > 0:
                print(f'missing: {pkg}')
                missing_count += 1
        print(f'total {len(pkg_list)}, missing {missing_count}')
