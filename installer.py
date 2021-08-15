from enum import Enum
import scripts

INSTALLER_FLAGS = '-Syu --needed --noconfirm'
MULTILINE_SEP = ' \\\n\t'

class Installer(str, Enum):
    pacman = 'pacman'
    yay = 'yay'

    def with_flags(self) -> str:
        return self + INSTALLER_FLAGS

    def to_script(self, pkg_list: list[str]) -> str:
        call = MULTILINE_SEP.join([self.with_flags()] + pkg_list)
        if self == Installer.yay:
            call = scripts.INSTALL_YAY + '\n' + call
        return call
