from enum import Enum
import templates

INSTALLER_FLAGS = '-Syu --needed --noconfirm'
MULTILINE_SEP = ' \\\n\t'

class Installer(str, Enum):
    PACMAN = 'sudo pacman'
    YAY = 'yay'

    def with_flags(self) -> str:
        return self + ' ' + INSTALLER_FLAGS

    def script(self, pkg_list: list[str]) -> str:
        call = MULTILINE_SEP.join([self.with_flags()] + pkg_list)
        if self == Installer.YAY:
            call = templates.INSTALL_YAY + '\n' + call
        return call
