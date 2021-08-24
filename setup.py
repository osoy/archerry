from os import path, mkdir
from threading import Thread
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
    started_at: float = time()

    def __init__(self, spec: Specification, dist_dir='.'):
        self.dist_dir = dist_dir
        self.spec = spec
        self.pref = Preferences.from_dict(spec)
        self.disk = DiskSetup.from_dict(spec)

    def input_missing(self):
        self.pref.input_missing()
        self.disk.input_missing()

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

    def passed(self) -> str:
        return fmt_seconds(int(time() - self.started_at))

    def print_status(self):
        moment = datetime.now().strftime('%H:%M:%S')
        passed = self.passed()
        state = self.read_state()
        usage = mnt_usage()
        print_status(usage, f'{passed} {moment}', state)

    def exec_dist(self):
        proc = Popen(
            ['bash', f'{self.dist_dir}/main.bash'],
            stdout=PIPE,
            stderr=STDOUT)
        while line := proc.stdout.readline().decode('utf-8'):
            print(line, end='')
            self.print_status()
            with open('archerry.log', 'a') as file: file.write(line)

    def run(self):
        self.started_at = time()
        run(['rm', '-f', 'archerry.log'])
        thread = Thread(target=self.exec_dist)
        thread.start()
        while thread.is_alive():
            self.print_status()
            sleep(.5)
        run(['mv', 'archerry.log', '/mnt/var/log'])
        print(f'Completed in {self.passed()}')
