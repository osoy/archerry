from enum import Enum
from typing import Optional
from os.path import exists
from subprocess import run, PIPE
from table import Table, TableKind
from partition import Partition
from ui import input_choice, input_natural
import templates

def efi_exists() -> bool:
    return exists('/sys/firmware/efi')

def available_disks() -> list[[str, int]]:
    proc = run(['bash', '-c', templates.DISKS], stdout = PIPE)
    disks = []
    for line in proc.stdout.decode('utf-8').split('\n')[0:-1]:
        path, size = line.split(' ')
        try:
            size = int(size)
            if size > 0: disks.append([path, int(size)])
        except: pass
    return disks

def input_disk_device() -> str:
    disks = available_disks()
    if len(disks) < 1: raise Exception('No disks found')
    str_of_disk = lambda disk : '- %s (%sMiB)' % \
        (disk[0], int(disk[1] / 1024 / 1024))
    print('\n'.join(map(str_of_disk, disks)))
    disk_paths = set(map(lambda disk : disk[0], disks))
    chosen = input_choice('device', disk_paths)
    return chosen

class DiskSetup:
    device: str
    efi_size_mb: int
    swap_size_mb: int

    def __init__(self, dev: str, efi: int, swap: int):
        self.device = dev
        self.efi_size_mb = efi
        self.swap_size_mb = swap

    @classmethod
    def from_input(cls):
        device = input_disk_device()
        efi_size = (0, 512) [efi_exists()]
        swap_size = input_natural('optional swap size (MiB)')
        return DiskSetup(device, efi_size, swap_size)

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