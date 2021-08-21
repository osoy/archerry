from os import path, mkdir
from disk import DiskSetup
from specification import Specification
from ui import input_file, input_secret, input_word
import templates

class Setup:
    disk: DiskSetup
    spec: Specification
    hostname: str
    username: str
    password: str

    @classmethod
    def from_input(cls):
        setup = Setup()
        spec_path = input_file('config file')
        setup.spec = Specification.from_file(spec_path)
        setup.disk = DiskSetup.from_input()
        setup.hostname = input_word('hostname')
        setup.username = input_word('username')
        setup.password = input_secret('password')
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
                user=self.username),
        ])

    def root_script(self):
        return '\n\n\n'.join([
            templates.SCRIPT_HEAD,
            templates.SETUP_CLOCK,
            templates.SETUP_HOST.substitute(hostname=self.hostname),
            templates.SETUP_LOCALE,
            templates.SETUP_PACMAN,
            self.disk.bootloader_script(),
            templates.INSTALL_NET,
            templates.SETUP_USER.substitute(
                name=self.username,
                password=self.password),
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
