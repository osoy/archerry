from enum import Enum
from typing import Optional
import templates

class PartitionKind(str, Enum):
    EFI = 'ESP fat32'
    SWAP = 'primary linux-swap'
    ROOT = 'primary'

    def format_script(self, device: str) -> str:
        if self == PartitionKind.EFI: return f'mkfs.fat -F32 {device}\n'
        elif self == PartitionKind.SWAP: return f'mkswap {device}\n'
        elif self == PartitionKind.ROOT: return f'mkfs.ext4 {device}\n'

    def mount_script(self, device: str) -> str:
        if self == PartitionKind.ROOT:
            return templates.MOUNT.substitute(device=device, path='/mnt')
        elif self == PartitionKind.EFI:
            return templates.MOUNT.substitute(device=device, path='/mnt/boot')
        elif self == PartitionKind.SWAP:
            return f'swapon {device}\n'

    def fstab_options(self) -> str:
        if self == PartitionKind.ROOT: return '/ ext4 defaults 0 1'
        elif self == PartitionKind.EFI: return '/boot vfat defaults 0 2'
        elif self == PartitionKind.SWAP: return 'none swap defaults 0 0'

    def fstab_entry_script(self, device: str) -> str:
        return 'UUID=$(%s) %s' % (
            templates.BLK_UUID.substitute(device=device).strip(),
            self.fstab_options())

class Partition:
    kind: PartitionKind
    size_mb: Optional[int]

    def __init__(self, kind: PartitionKind, size_mb: Optional[int]):
        self.kind = kind
        self.size_mb = size_mb

    @classmethod
    def efi(cls, size_mb: int):
        return Partition(PartitionKind.EFI, size_mb)

    @classmethod
    def swap(cls, size_mb: int):
        return Partition(PartitionKind.SWAP, size_mb)

    @classmethod
    def root(cls):
        return Partition(PartitionKind.ROOT, None)

    @classmethod
    def device(cls, disk: str, i: int) -> str:
        return disk + (str(i), 'p' + str(i)) [disk[-1].isdigit()]

    def size(self) -> str:
        if self.size_mb: return f'{self.size_mb}MiB'
        else: return '100%'

    def script(self, device: str, start: int) -> str:
        return templates.PARTED.substitute(
            device=device,
            command=f'mkpart {self.kind} {start}MiB {self.size()}')
