from string import Template

SCRIPT_HEAD = '#!/bin/bash'

CWD = '''
cd "$(dirname "$(readlink -f "$0")")"
'''

STATUS = Template('''
printf '\\n[%s] $msg\\n\\n' "$$(date +%FT%T)"
echo '$msg' > state
''')

PARTED = Template('''
parted -s $device -- $command
''')

DISKS = '''
lsblk -bo type,path,size |
	sed -n 's/^disk \+\([^ ]\+\) \+\([^ ]*\).*$/\\1 \\2/p'
'''

MEMORY = '''
free -b | sed -n 's/^Mem: *\([^ ]\+\) .*$/\\1/p'
'''

MNT_USAGE = '''
df -B 1 | sed -n 's|^[^ ]\+ \+[^ ]\+ \+\([^ ]\+\) .\+ /mnt$|\\1|p'
'''

BATTERY = '''
find /sys/class/power_supply/BAT* -maxdepth 0 2>/dev/null | while read -r bat
do printf '%i %i %i\\n' \\
	$(cat "$bat/charge_now") \\
    $(cat "$bat/charge_full") \\
	$(cat "$bat/status" | grep -c Charging)
done
'''

BLK_UUID = Template('''
lsblk -o path,uuid | sed -n 's|^$device \+\(.*\)$$|\\1|p'
''')

MOUNT = Template('''
mkdir -p $path
mount $device $path
''')

CHROOT = Template('''
cp $file /mnt
arch-chroot /mnt bash /$file
rm -f /mnt/$file
''')

CHROOT_USER = Template('''
cp $file /mnt
arch-chroot /mnt runuser -l $user -c 'cd; bash /$file'
rm -f /mnt/$file
''')

SETUP_CLOCK = '''
timedatectl set-ntp true
hwclock --systohc
'''

RANK_MIRRORS = '''
pacman -Sy --needed --noconfirm pacman-contrib
cp /etc/pacman.d/mirrorlist{,.bak}
rankmirrors /etc/pacman.d/mirrorlist.bak |
	grep -v '^#' > /etc/pacman.d/mirrorlist
'''

PACSTRAP = '''
pacstrap /mnt linux{,-firmware} base{,-devel} grub sudo vi git
'''

SETUP_SUDO = '''
usermod -aG wheel root
echo '%wheel ALL=(ALL) NOPASSWD:ALL' > /mnt/etc/sudoers
trap "echo '%wheel ALL=(ALL) ALL' > /mnt/etc/sudoers" EXIT
'''

SETUP_USER = Template('''
useradd -m $name
echo '$name:$password' | chpasswd
usermod -aG wheel $name
''')

SETUP_PACMAN = '''
[ $(grep -c '^\[multilib\]' /etc/pacman.conf) -lt 1 ] &&
echo '[multilib]
Include = /etc/pacman.d/mirrorlist' >> /etc/pacman.conf
pacman -Syu
'''

SETUP_BOOTLOADER = Template('''
pacman -Sy --needed --noconfirm grub
grub-install --target=i386-pc --boot-directory=/boot $device
grub-mkconfig -o /boot/grub/grub.cfg
''')

SETUP_BOOTLOADER_EFI = '''
pacman -Sy --needed --noconfirm grub efibootmgr
grub-install --target=x86_64-efi --efi-directory=/boot
grub-mkconfig -o /boot/grub/grub.cfg
'''

SETUP_HOST = Template('''
echo '127.0.0.1 localhost
::1 localhost
127.0.1.1 $hostname.localdomain $hostname' > /etc/hosts
echo '$hostname' > /etc/hostname
''')

SETUP_LOCALE = '''
echo 'LANG=en_US.UTF-8' | sudo tee /etc/locale.conf
echo 'en_US.UTF-8 UTF-8' | sudo tee /etc/locale.gen
sudo locale-gen
'''

TIMEZONES = '''
timedatectl list-timezones
'''

SETUP_TIMEZONE = Template('''
sudo timedatectl set-timezone $timezone
''')

INSTALL_YAY = '''
git clone https://aur.archlinux.org/yay-bin.git ~/.cache/yay/yay-bin &&
	(cd ~/.cache/yay/yay-bin && makepkg -si --noconfirm)
'''
