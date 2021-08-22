from os import path, mkdir
from subprocess import run, CompletedProcess
from disk import DiskSetup
from specification import Specification
from preferences import Preferences
from utils import concat
from templates import *

class Setup:
    disk: DiskSetup
    pref: Preferences
    spec: Specification
    dist_dir: str

    def __init__(self, spec_file: str, dist_dir='.'):
        self.dist_dir = dist_dir
        self.spec = Specification.from_file(spec_file)

    def input(self):
        self.disk = DiskSetup.from_input()
        self.pref = Preferences.from_input()

    def iso_script(self) -> str:
        return concat([
            SCRIPT_HEAD,
            CWD,
            STATUS.substitute(msg='Disk setup'),
            self.disk.table_script(),
            STATUS.substitute(msg='Ranking mirrors'),
            SETUP_CLOCK,
            RANK_MIRRORS,
            STATUS.substitute(msg='Pacstrap'),
            PACSTRAP,
            SETUP_SUDO,
            STATUS.substitute(msg='As root'),
            CHROOT.substitute(file='root.bash'),
            STATUS.substitute(msg='As user'),
            CHROOT_USER.substitute(
                file='user.bash',
                user=self.pref.username),
            STATUS.substitute(msg='Done'),
        ], 2)

    def root_script(self) -> str:
        return concat([
            SCRIPT_HEAD,
            SETUP_CLOCK,
            SETUP_LOCALE,
            SETUP_PACMAN,
            self.pref.script(),
            self.disk.bootloader_script(),
        ], 2)

    def user_script(self) -> str:
        return concat([
            SCRIPT_HEAD,
            self.spec.script(),
        ], 2)

    def write_dist(self):
        if not path.isdir(self.dist_dir): mkdir(self.dist_dir)
        with open(f'{self.dist_dir}/main.bash', 'w') as file:
            file.write(self.iso_script())
        with open(f'{self.dist_dir}/root.bash', 'w') as file:
            file.write(self.root_script())
        with open(f'{self.dist_dir}/user.bash', 'w') as file:
            file.write(self.user_script())

    def exec_dist(self) -> CompletedProcess:
        return run(
            f'bash {self.dist_dir}/main.bash | tee archerry.log',
            shell=True)

    def run(self):
        self.exec_dist()
        run(['mv', 'archerry.log', '/mnt/var/log'])
