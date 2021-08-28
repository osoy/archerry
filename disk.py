from enum import Enum
from typing import Optional
from os.path import exists

from table import Table, TableKind
from partition import Partition
from ui import input_index, input_natural, bin_unit, table
from utils import bash_pipe, bash_lines
import templates

def efi_exists() -> bool:
    return exists('/sys/firmware/efi')

def available_disks() -> list[[str, int]]:
    disks = []
    for line in bash_lines(templates.DISKS):
        path, size = line.split()
        try:
            size = int(size)
            if size > 0: disks.append([path, int(size)])
        except: pass
    return disks

def print_disks(disks: list[[str, int]]):
    rows = [['Nr', 'Path', 'Size']]
    for i, disk in enumerate(disks):
        rows.append([str(i), disk[0], bin_unit(disk[1])])
    print(table(rows))

def input_disk_device() -> str:
    disks = available_disks()
    if len(disks) < 1: raise Exception('No disks found')
    print_disks(disks)
    chosen = input_index('Device (nr)', disks)[0]
    return chosen

def input_swap_size_mb() -> int:
    print('Detected memory ' + bin_unit(int(bash_pipe(templates.MEMORY))))
    return input_natural('Swap size in MiB (optional)', True)

class DiskSetup:
    device: Optional[str] = None
    efi_size_mb: int = (0, 512) [efi_exists()]
    swap_size_mb: Optional[int] = None

    @classmethod
    def from_dict(cls, obj: dict):
        disk_setup = DiskSetup()
        disk_setup.device = obj.get('disk')
        try: disk_setup.swap_size_mb = int(obj.get('swap'))
        except: pass
        return disk_setup

    def input_missing(self):
        if not self.device: self.device = input_disk_device()
        if self.swap_size_mb == None: self.swap_size_mb = input_swap_size_mb()

    def table(self) -> Table:
        kind = TableKind.MBR
        partitions = [Partition.root()]
        if self.swap_size_mb:
            partitions = [Partition.swap(self.swap_size_mb)] + partitions
        if self.efi_size_mb:
            kind = TableKind.GPT
            partitions = [Partition.efi(self.efi_size_mb)] + partitions
        return Table(kind, partitions)

    def bootloader_script(self) -> str:
        if efi_exists(): return templates.SETUP_BOOTLOADER_EFI
        else: return templates.SETUP_BOOTLOADER.substitute(device=self.device)

    def table_script(self) -> str:
        return self.table().script(self.device)
