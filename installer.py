from enum import Enum
from subprocess import run, DEVNULL
from utils import concat
import templates

class Installer(str, Enum):
    PACMAN = 'sudo pacman'
    YAY = 'yay'

    def add_cmd(self) -> str:
        return f'{self} -Syu --needed --noconfirm'

    def script(self, pkg_list: list[str]) -> str:
        call = concat([self.add_cmd()] + pkg_list, 0)
        if self == Installer.YAY:
            call = concat([templates.INSTALL_YAY, call], 2)
        return call

    def check(self, pkg_list: list[str]) -> int:
        if self == Installer.YAY: pkg_list.append('yay')
        missing_count = 0
        for pkg in pkg_list:
            proc = run(
                f'pacman -Q {pkg} || pacman -Qg {pkg}',
                stdout=DEVNULL,
                stderr=DEVNULL,
                shell=True)
            if proc.returncode < 0: exit(1)
            elif proc.returncode > 0:
                print(f'Missing: {pkg}')
                missing_count += 1
        print(f'Total {len(pkg_list)}, Missing {missing_count}')
        return missing_count
