from os import path, mkdir
from subprocess import Popen, run, PIPE, STDOUT
from time import time, sleep
from datetime import datetime

from disk import DiskSetup
from specification import Specification
from preferences import Preferences
from utils import concat, bash_pipe
from ui import print_status, fmt_seconds, bin_unit
from templates import *

def mnt_usage() -> str:
    try: return bin_unit(int(bash_pipe(MNT_USAGE)))
    except: return ''

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

    def read_state(self) -> str:
        try:
            with open(f'{self.dist_dir}/state') as file:
                return file.read().strip()
        except: return ''

    def run(self):
        start = time()
        run(['rm', '-f', 'archerry.log'])
        proc = Popen(
            f'bash {self.dist_dir}/main.bash | tee archerry.log',
            stdout=PIPE,
            stderr=STDOUT,
            shell=True)
        while line := proc.stdout.readline().decode('utf-8'):
            passed = fmt_seconds(int(time() - start))
            moment = datetime.now().strftime('%H:%M:%S')
            state = self.read_state()
            usage = mnt_usage()
            print(line, end='')
            print_status(usage, f'{passed} {moment}', state)
        run(['mv', 'archerry.log', '/mnt/var/log'])
        print(f'Completed in {moment}')
