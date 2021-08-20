from string import Template

SCRIPT_HEAD = '#!/bin/sh'

WRITE = Template('''
mkdir -p "$$(dirname $path)"
printf '$content' > $path
''')

PARTED = Template('''
parted -s $device -- $command
''')

LIST_DISKS = '''
lsblk -bo type,name,size | sed -n 's/^disk \+\([^ ]\+\) \+\([^ ]*\).*$/\\1 \\2/p'
'''

MOUNT = Template('''
mkdir -p $path
mount $device $path
''')

SETUP_CLOCK = '''
timedatectl set-ntp true
hwclock --systohc
'''

RANK_MIRRORS = '''
pacman -Sy --needed --noconfirm pacman-contrib
cp /etc/pacman.d/mirrorlist{,.bak}
rankmirrors /etc/pacman.d/mirrorlist.bak | grep -v '^#' > /etc/pacman.d/mirrorlist
'''

PACSTRAP = Template('''
pacstrap '$mnt' linux{,-firmware} base{,-devel} grup sudo vi git
''')

SETUP_BOOTLOADER = Template('''
echo '$fstab' > /etc/fstab
pacman -Sy --needed --noconfirm grub
if [ -e /sys/firmware/efi ]
then
	pacman -Sy --needed --noconfirm efibootmgr
	grub-install --target=x86_64-efi --efi-directory=/boot
else
	grub-install --target=i386-pc --boot-directory=/boot $device
fi
grub-mkconfig -o /boot/grub/grub.cfg
''')

INSTALL_NET = Template('''
pacman -Sy --needed --noconfirm dhcpcd wpa_supplicant
systemctl enable dhcpcd
''')

SETUP_PACMAN = '''
[ $(grep -c '^[multilib]' /etc/pacman.conf) -lt 1 ] &&
echo '[multilib]
Include = /etc/pacman.d/mirrorlist' >> /etc/pacman.conf
pacman -Syu
'''

SETUP_HOST = Template('''
echo '127.0.0.1 localhost
::1 localhost
127.0.1.1 $hostname.localdomain $hostname' > /etc/hosts
echo '$hostname' > /etc/hostname
''')

SETUP_TIMEZONE = Template('''
ln -sf '$path' /etc/localtime
''')

SETUP_LOCALE = '''
echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen
locale-gen
echo 'LANG=en_US.UTF-8' > /etc/locale.conf
'''

BIND_SUDO = Template('''
echo '%wheel ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers
trap "echo '%wheel ALL=(ALL) ALL' > /etc/sudoers" EXIT
''')

SETUP_ROOT = Template('''
echo 'root:$password' | chpasswd
usermod -aG wheel root
''')

SETUP_USER = Template('''
useradd -m $name
echo '$name:$password' | chpasswd
usermod -aG wheel $name
''')

INSTALL_YAY = '''
git clone https://aur.archlinux.org/yay-bin.git ~/.cache/yay/yay-bin
cd ~/.cache/yay/yay-bin
makepkg -si --noconfirm
'''
