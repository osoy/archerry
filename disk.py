from enum import Enum
from typing import Optional
from os.path import exists
from subprocess import run, PIPE
from table import Table, TableType, Partition
from ui import input_choice, input_natural
import templates

def efi_exists() -> bool:
    return exists('/sys/firmware/efi')

def available_disks() -> list[[str, int]]:
    proc = run(['bash', '-c', templates.LIST_DISKS], stdout = PIPE)
    disks = []
    for line in proc.stdout.decode('utf-8').split('\n')[0:-1]:
        name, size = line.split(' ')
        try:
            size = int(size)
            if size > 0: disks.append([name, int(size)])
        except: pass
    return disks

def input_disk_device() -> str:
    disks = available_disks()
    if len(disks) < 1: raise Exception('No disks found')
    str_of_disk = lambda disk : '- %s (%sMiB)' % \
        (disk[0], int(disk[1] / 1024 / 1024))
    print('\n'.join(map(str_of_disk, disks)))
    chosen = input_choice('device', set(map(lambda disk : disk[0], disks)))
    return '/dev/' + chosen

class Disk:
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
        return Disk(device, efi_size, swap_size)

    def to_table(self) -> Table:
        table_type = TableType.MBR
        partitions = [Partition.root()]
        if self.swap_size_mb:
            partitions = [Partition.swap(self.swap_size_mb)] + partitions
        if self.efi_size_mb:
            table_type = TableType.GPT
            partitions = [Partition.efi(self.efi_size_mb)] + partitions
        return Table(table_type, partitions)

    def to_script(self) -> str:
        return '\n\n\n'.join([
            templates.SCRIPT_HEAD,
            self.to_table().to_script(self.device)
        ])
