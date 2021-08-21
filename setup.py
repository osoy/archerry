from os import path, mkdir
from disk import DiskSetup
from specification import Specification
from preferences import Preferences
from utils import cat
import templates

class Setup:
    disk: DiskSetup
    pref: Preferences
    spec: Specification

    @classmethod
    def from_input(cls):
        setup = Setup()
        setup.disk = DiskSetup.from_input()
        setup.pref = Preferences.from_input()
        setup.spec = Specification.from_input()
        return setup

    def iso_script(self):
        return cat([
            templates.SCRIPT_HEAD,
            templates.CWD,
            self.disk.table_script(),
            templates.SETUP_CLOCK,
            templates.RANK_MIRRORS,
            templates.PACSTRAP,
            templates.SETUP_SUDO,
            templates.CHROOT.substitute(file='root.sh'),
            templates.CHROOT_USER.substitute(
                file='user.sh',
                user=self.pref.username),
        ], 2)

    def root_script(self):
        return cat([
            templates.SCRIPT_HEAD,
            templates.SETUP_CLOCK,
            templates.SETUP_LOCALE,
            templates.SETUP_PACMAN,
            self.pref.script(),
            self.disk.bootloader_script(),
        ], 2)

    def user_script(self):
        return cat([
            templates.SCRIPT_HEAD,
            self.spec.script(),
        ], 2)

    def write_dist(self, dist_dir = 'dist'):
        if not path.isdir(dist_dir): mkdir(dist_dir)
        with open(f'{dist_dir}/iso.sh', 'w') as file:
            file.write(self.iso_script())
        with open(f'{dist_dir}/root.sh', 'w') as file:
            file.write(self.root_script())
        with open(f'{dist_dir}/user.sh', 'w') as file:
            file.write(self.user_script())
