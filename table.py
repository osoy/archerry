from enum import Enum
from partition import Partition
import templates
from utils import cat

class TableKind(str, Enum):
    GPT = 'gpt'
    MBR = 'msdos'

    def script(self, device: str):
        return templates.PARTED.substitute(
            device=device,
            command=f'mklabel {self}')

class Table:
    kind: TableKind
    partitions: list[Partition]

    def __init__(self, kind: TableKind, partitions: list[Partition]):
        self.kind = kind
        self.partitions = partitions

    def partition_script(self, device: str) -> str:
        cmds = [self.kind.script(device)]
        pointer = 1
        for partition in self.partitions:
            cmds.append(partition.script(device, pointer))
            if partition.size_mb: pointer += partition.size_mb
            else: break
        return cat(cmds)

    def format_script(self, device: str) -> str:
        cmds = []
        for i, partition in enumerate(self.partitions):
            cmds.append(partition.kind.format_script(
                Partition.device(device, i + 1)))
        return cat(cmds)

    def mount_script(self, device: str) -> str:
        cmds = []
        for i, partition in enumerate(self.partitions):
            cmds.append(partition.kind.mount_script(
                Partition.device(device, i + 1)))
        return cat(cmds)

    def fstab_script(self, device: str) -> str:
        entries = []
        for i, partition in enumerate(self.partitions):
            entries.append(partition.kind.fstab_entry_script(
                Partition.device(device, i + 1)))
        return cat([
            'mkdir -p /mnt/etc',
            f'echo "{cat(entries)}" > /mnt/etc/fstab',
        ])

    def script(self, device: str) -> str:
        return cat([
            self.partition_script(device),
            self.format_script(device),
            self.mount_script(device),
            self.fstab_script(device),
        ], 2)
