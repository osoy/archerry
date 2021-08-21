from os import path, mkdir
from disk import DiskSetup
from specification import Specification
from preferences import Preferences
import templates

class Setup:
    disk: DiskSetup
    spec: Specification
    pref: Preferences

    @classmethod
    def from_input(cls):
        setup = Setup()
        setup.spec = Specification.from_input()
        setup.disk = DiskSetup.from_input()
        setup.pref = Preferences.from_input()
        return setup

    def iso_script(self):
        return '\n\n\n'.join([
            templates.SCRIPT_HEAD,
            self.disk.table_script(),
            templates.SETUP_CLOCK,
            templates.RANK_MIRRORS,
            templates.PACSTRAP,
            templates.CHROOT.substitute(file='root.sh'),
            templates.BIND_SUDO,
            templates.CHROOT_USER.substitute(
                file='user.sh',
                user=self.pref.username),
        ])

    def root_script(self):
        return '\n\n\n'.join([
            templates.SCRIPT_HEAD,
            templates.SETUP_CLOCK,
            templates.SETUP_LOCALE,
            templates.SETUP_PACMAN,
            self.pref.script(),
            self.disk.bootloader_script(),
            templates.INSTALL_NET,
        ])

    def user_script(self):
        return '\n\n\n'.join([
            templates.SCRIPT_HEAD,
            self.spec.user_script(),
        ])

    def write_dist(self, dist_dir = 'dist'):
        if not path.isdir(dist_dir): mkdir(dist_dir)
        with open(f'{dist_dir}/iso.sh', 'w') as f: f.write(self.iso_script())
        with open(f'{dist_dir}/root.sh', 'w') as f: f.write(self.root_script())
        with open(f'{dist_dir}/user.sh', 'w') as f: f.write(self.user_script())
