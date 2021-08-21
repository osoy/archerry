from enum import Enum
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
