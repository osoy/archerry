from enum import Enum
from partition import Partition
import templates

class TableKind(str, Enum):
    GPT = 'gpt'
    MBR = 'msdos'

    def script(self, device: str):
        return templates.PARTED.substitute(
            device = device,
            command = 'mklabel ' + self)

class Table:
    kind: TableKind
    partitions: list[Partition]

    def __init__(self, kind: TableKind, partitions: list[Partition]):
        self.kind = kind
        self.partitions = partitions

    def partition_script(self, device: str) -> str:
        result = self.kind.script(device)
        pointer = 1
        for partition in self.partitions:
            result += partition.script(device, pointer)
            if partition.size_mb: pointer += partition.size_mb
            else: break
        return result

    def format_script(self, device: str) -> str:
        result = ''
        for i, partition in enumerate(self.partitions):
            result += partition.kind.format_script(
                Partition.device(device, i + 1))
        return result

    def mount_script(self, device: str) -> str:
        result = ''
        for i, partition in enumerate(self.partitions):
            result += partition.kind.mount_script(
                Partition.device(device, i + 1))
        return result

    def fstab_script(self, device: str) -> str:
        entries = []
        for i, partition in enumerate(self.partitions):
            entries.append(partition.kind.fstab_entry_script(
                Partition.device(device, i + 1)))
        return templates.WRITEX.substitute(
            path = '/mnt/etc/fstab',
            content = '\n'.join(entries))

    def script(self, device: str) -> str:
        return '\n\n\n'.join([
            self.partition_script(device),
            self.format_script(device),
            self.mount_script(device),
            self.fstab_script(device),
        ])
