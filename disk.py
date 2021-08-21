from enum import Enum
from typing import Optional
from os.path import exists
from table import Table, TableKind
from partition import Partition
from ui import input_choice, input_natural
from utils import bash_out, bash_lines, prefix_bin
import templates

def efi_exists() -> bool:
    return exists('/sys/firmware/efi')

def available_disks() -> list[[str, int]]:
    disks = []
    for line in bash_lines(templates.DISKS):
        path, size = line.split(' ')
        try:
            size = int(size)
            if size > 0: disks.append([path, int(size)])
        except: pass
    return disks

def input_disk_device() -> str:
    disks = available_disks()
    if len(disks) < 1: raise Exception('No disks found')
    str_of_disk = lambda disk : '- %s (%s)' % (disk[0], prefix_bin(disk[1]))
    print('\n'.join(['Available disks:'] + list(map(str_of_disk, disks))))
    disk_paths = set(map(lambda disk : disk[0], disks))
    chosen = input_choice('Device', disk_paths)
    return chosen

def input_swap_size_mb() -> int:
    print('Detected memory ' + prefix_bin(int(bash_out(templates.MEMORY))))
    return input_natural('Swap size in MiB (optional)')

class DiskSetup:
    device: str
    efi_size_mb: int
    swap_size_mb: int

    @classmethod
    def from_input(cls):
        disk_setup = DiskSetup()
        disk_setup.device = input_disk_device()
        disk_setup.efi_size_mb = (0, 512) [efi_exists()]
        disk_setup.swap_size_mb = input_swap_size_mb()
        return disk_setup

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
