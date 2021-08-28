from os import path, mkdir
from sys import stdout
from threading import Thread
from subprocess import Popen, run, PIPE, STDOUT
from time import time, sleep
from datetime import datetime

from disk import DiskSetup
from specification import Specification
from preferences import Preferences
from utils import concat, bash_pipe, write_file
from ui import status_bar, fmt_seconds, bin_unit
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
    user_only = False
    state = ''
    state_ts = 0
    usage = ''
    usage_ts = 0

    def __init__(self, spec: Specification, dist_dir='.'):
        self.dist_dir = dist_dir
        self.spec = spec
        self.pref = Preferences.from_dict(spec)
        self.disk = DiskSetup.from_dict(spec)

    def user_only(self):
        self.user_only = True

    def input_missing(self):
        self.pref.input_missing()
        self.disk.input_missing()

    def main_script(self) -> str:
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

    def write_dist_init(self):
        write_file(f'{self.dist_dir}/main.bash', self.main_script())
        write_file(f'{self.dist_dir}/root.bash', self.root_script())

    def write_dist_user(self):
        write_file(f'{self.dist_dir}/user.bash', self.user_script())

    def write_dist(self):
        if not self.user_only: self.write_dist_init()
        self.write_dist_user()

    def read_state(self):
        if time() - self.state_ts < 1: return
        try:
            self.state_ts = time()
            with open(f'{self.dist_dir}/state') as file:
                self.state = file.readline().strip()
        except: return

    def read_usage(self):
        if time() - self.usage_ts < 1: return
        self.usage_ts = time()
        self.usage = mnt_usage()

    def passed(self) -> str:
        return fmt_seconds(int(time() - self.started_at))

    def status_bar(self) -> str:
        moment = datetime.now().strftime('%H:%M:%S')
        passed = self.passed()
        self.read_usage()
        self.read_state()
        return status_bar(self.usage, f'{passed} {moment}', self.state)

    def exec_dist(self):
        entry = ('main', 'user') [self.user_only]
        proc = Popen(
            ['bash', f'{self.dist_dir}/{entry}.bash'],
            stdout=PIPE,
            stderr=STDOUT)
        while line := proc.stdout.readline().decode('utf-8'):
            stdout.write(line + self.status_bar())
            stdout.flush()
            with open('archerry.log', 'a') as file: file.write(line)

    def run(self):
        self.started_at = time()
        run(['rm', '-f', 'archerry.log'])
        thread = Thread(target=self.exec_dist)
        thread.start()
        while thread.is_alive():
            stdout.write(self.status_bar())
            stdout.flush()
            sleep(.5)
        run(['mv', 'archerry.log', '/mnt/var/log'])
        print(f'Completed in {self.passed()}')
