from os import path, mkdir
from disk import DiskSetup
from specification import Specification
from preferences import Preferences
from utils import cat
from templates import *

class Setup:
    disk: DiskSetup
    pref: Preferences
    spec: Specification

    @classmethod
    def from_input(cls):
        setup = Setup()
        setup.spec = Specification.from_args()
        setup.disk = DiskSetup.from_input()
        setup.pref = Preferences.from_input()
        return setup

    def iso_script(self):
        return cat([
            SCRIPT_HEAD,
            CWD,
            TS.substitute(msg='Disk setup'),
            self.disk.table_script(),
            TS.substitute(msg='Rank mirrors'),
            SETUP_CLOCK,
            RANK_MIRRORS,
            TS.substitute(msg='Pacstrap'),
            PACSTRAP,
            SETUP_SUDO,
            TS.substitute(msg='Chroot'),
            CHROOT.substitute(file='root.bash'),
            CHROOT_USER.substitute(
                file='user.bash',
                user=self.pref.username),
        ], 2)

    def root_script(self):
        return cat([
            SCRIPT_HEAD,
            SETUP_CLOCK,
            SETUP_LOCALE,
            SETUP_PACMAN,
            self.pref.script(),
            TS.substitute(msg='Bootloader'),
            self.disk.bootloader_script(),
        ], 2)

    def user_script(self):
        return cat([
            SCRIPT_HEAD,
            TS.substitute(msg='Specification'),
            self.spec.script(),
        ], 2)

    def write_dist(self, dist_dir='.'):
        if not path.isdir(dist_dir): mkdir(dist_dir)
        with open(f'{dist_dir}/main.bash', 'w') as file:
            file.write(self.iso_script())
        with open(f'{dist_dir}/root.bash', 'w') as file:
            file.write(self.root_script())
        with open(f'{dist_dir}/user.bash', 'w') as file:
            file.write(self.user_script())
