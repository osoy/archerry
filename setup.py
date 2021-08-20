from os import path
from disk import DiskSetup
from specification import Specification
from ui import input_file

class Setup:
    disk: DiskSetup
    spec: Specification

    def __init__(self, disk: DiskSetup, spec: Specification):
        self.disk = disk
        self.spec = spec

    @classmethod
    def from_input(cls):
        spec_path = input_file('config file')
        spec = Specification.from_file(spec_path)
        disk = DiskSetup.from_input()
        return Setup(disk, spec)

    def write_dist(self, dist_dir = 'dist'):
        if not path.isdir(dist_dir): mkdir(dist_dir)
        with open('dist/root.sh', 'w') as file:
            file.write(self.disk.table_script())
        with open('dist/chroot.sh', 'w') as file:
            file.write('\n\n\n'.join([
                self.disk.bootloader_script(),
                self.spec.script(),
            ]))
