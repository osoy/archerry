from enum import Enum
from typing import Optional
import templates

class PartitionType(str, Enum):
    EFI = 'ESP fat32'
    SWAP = 'primary linux-swap'
    ROOT = 'primary'

    def format_script(self, device: str) -> str:
        if self == PartitionType.EFI: return f'mkfs.fat -F32 {device}\n'
        elif self == PartitionType.SWAP: return f'mkswap {device}\n'
        elif self == PartitionType.ROOT: return f'mkfs.ext4 {device}\n'

    def mount_script(self, device: str) -> str:
        if self == PartitionType.ROOT:
            return templates.MOUNT.substitute(device=device, path='/mnt')
        elif self == PartitionType.EFI:
            return templates.MOUNT.substitute(device=device, path='/mnt/boot')
        elif self == PartitionType.SWAP:
            return f'swapon {device}\n'

class Partition:
    part_type: PartitionType
    size_mb: Optional[int]

    def __init__(self, part_type: PartitionType, size_mb: Optional[int]):
        self.part_type = part_type
        self.size_mb = size_mb

    @classmethod
    def efi(cls, size_mb: int):
        return Partition(PartitionType.EFI, size_mb)

    @classmethod
    def swap(cls, size_mb: int):
        return Partition(PartitionType.SWAP, size_mb)

    @classmethod
    def root(cls):
        return Partition(PartitionType.ROOT, None)

    @classmethod
    def device(cls, disk: str, i: int) -> str:
        return disk + (str(i), 'p' + str(i)) [disk[-1].isdigit()]

    def size(self) -> str:
        if self.size_mb: return f'{self.size_mb}MiB'
        else: return '100%'

    def to_script(self, device: str, start: int) -> str:
        return templates.PARTED.substitute(
            device = device,
            command = f'mkpart {self.part_type} {start}MiB {self.size()}')

class TableType(str, Enum):
    GPT = 'gpt'
    MBR = 'msdos'

    def to_script(self, device: str):
        return templates.PARTED.substitute(
            device = device,
            command = 'mklabel ' + self)

class Table:
    table_type: TableType
    partitions: list[Partition]

    def __init__(self, table_type: TableType, partitions: list[Partition]):
        self.table_type = table_type
        self.partitions = partitions

    def partition_script(self, device: str) -> str:
        result = self.table_type.to_script(device)
        pointer = 1
        for partition in self.partitions:
            result += partition.to_script(device, pointer)
            if partition.size_mb: pointer += partition.size_mb
            else: break
        return result

    def format_script(self, device: str) -> str:
        result = ''
        for i, partition in enumerate(self.partitions):
            result += partition.part_type.format_script(
                Partition.device(device, i + 1))
        return result

    def mount_script(self, device: str) -> str:
        result = ''
        for i, partition in enumerate(self.partitions):
            result += partition.part_type.mount_script(
                Partition.device(device, i + 1))
        return result

    def to_script(self, device: str) -> str:
        return '\n\n\n'.join([
            self.partition_script(device),
            self.format_script(device),
            self.mount_script(device),
        ])
