from enum import Enum
from subprocess import run, DEVNULL
from utils import concat
import templates

class Installer(str, Enum):
    PACMAN = 'sudo pacman'
    YAY = 'yay'

    def sync_cmd(self) -> str:
        return f'{self} --noconfirm -Syu'

    def add_cmd(self) -> str:
        return f'{self} --noconfirm -S --needed'

    def del_cmd(self) -> str:
        return f'{self} --noconfirm -Rnsdd'

    def script(self, pkg_list: list[str]) -> str:
        adds = []
        for pkg in pkg_list:
            if pkg[:7] == 'remove:': adds.append(f'{self.del_cmd()} {pkg[7:]}')
            else: adds.append(f'{self.add_cmd()} {pkg}')
        call = concat([self.sync_cmd()] + adds)
        if self == Installer.YAY:
            call = concat([templates.INSTALL_YAY, call], 2)
        return call

    def check(self, pkg_list: list[str]) -> int:
        if self == Installer.YAY: pkg_list.append('yay')
        missing_count = 0
        for pkg in pkg_list:
            if pkg[:7] == 'remove:': continue
            proc = run(
                ['bash', '-c', f'pacman -Q {pkg} || pacman -Qg {pkg}'],
                stdout=DEVNULL,
                stderr=DEVNULL)
            if proc.returncode > 0:
                print(f'Missing: {pkg}')
                missing_count += 1
        print('Total %i, Missing %i' % (len(pkg_list), missing_count))
        return missing_count
