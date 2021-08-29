# Archerry 🌸

[![Pipeline status](https://gitlab.com/osoy/archerry/badges/main/pipeline.svg)](https://gitlab.com/osoy/archerry/-/commits/main)
[![Coverage report](https://gitlab.com/osoy/archerry/badges/main/coverage.svg)](https://gitlab.com/osoy/archerry/-/commits/main)

Declerative Arch Linux installer.

## Features

- Basic partitioning
- Base install (kernel, firmware, base, bootloader)
- System setup from a human-readable specification file
- Incremental execution
- Tag selection

## Specification file

The system is configured with a [YAML](https://yaml.org) specification/config
file. Upon execution user is prompted to fill missing fields in the
specification and then shell scripts are composed from the specification and
run.

### Options

- `hostname` ‒ Hostname which is shown on the network
- `username` ‒ Username of the admin account
- `password` ‒ Password for the admin account  
  _Not recommended to store in spec_
- `timezone` ‒ Timezone keyword for
  [`timedatectl`](https://man.archlinux.org/man/timedatectl.1)
- `disk` ‒ Disk device path eg. `/dev/sda`  
  _Not recommended to store in spec since it may not be consistent_
- `swap` ‒ Swap size in MiB
- `yay` ‒ Whether to install and use `yay` for installing packages
- `pkg` ‒ Tree of packages
- `git` ‒ Tree of git repositories to clone
- `fs` ‒ Tree of files to write
- `cmd` ‒ Tree of commands to execute in the end

#### Example

Simple example of a specification file. See more at
[`rasmusmerzin/cfg-archerry`](https://gitlab.com/rasmusmerzin/cfg-archerry).

```yaml
hostname: MyLaptop
username: admin
timezone: Europe/Helsinki
swap: 1024
yay: true

pkg:
  - dhcpcd
  - tree neovim
  - xorg xorg-xinit dmenu slock feh
  - tag: emoji
    pkg: remove:libxft libxft-bgra ttf-twemoji

git:
  - repo: gitlab.com/rasmusmerzin/dwm
    path: ~/repos/dwm
  - repo: gitlab.com/rasmusmerzin/st
    path: ~/repos/st
  - tag: config
    git:
      - repo: gitlab.com/rasmusmerzin/cfg-nvim
        path: ~/repos/cfg-nvim
      - repo: gitlab.com/rasmusmerzin/cfg-bash
        path: ~/repos/cfg-bash

fs:
  - path: ~/.xinitrc
    write: |
      [ -x ~/.fehbg ] && ~/.fehbg
      exec dwm

cmd:
  - sudo systemctl enable dhcpcd
  - cd ~/repos/dwm && sudo make install
  - cd ~/repos/st && sudo make install
  - tag: config
    cmd:
      - cd ~/repos/cfg-nvim && make
      - cd ~/repos/cfg-bash && make
```

#### Tags

Tags are a way of making the specification file modular. Tags act similar to
CSS selectors. In the example by excluding config tag during execution
repositories `cfg-nvim` and `cfg-bash` are not cloned nor will `make` be run
for them.

### Usage

Currently the recommended way to use Archerry is as follows:

1. Boot with [Arch Linux ISO](https://archlinux.org/download)
2. Configure network (should be automatic when using ethernet).  
   When using Wi-Fi the easiest way to connect is
   ```bash
   wpa_supplicant -Bi <INTERFACE> -c <(wpa_passphrase <SSID> <PASSWORD>)
   ```
   See more at
   [ArchWiki wpa_supplicant](https://wiki.archlinux.org/title/Wpa_supplicant#Connecting_with_wpa_passphrase).
3. Install [Git](https://git-scm.com) with
   ```bash
   pacman -Sy git
   ```
4. Download Archerry with
   ```bash
   clone https://gitlab.com/osoy/archerry
   ```
5. Download your specification file with
   ```bash
   curl <URL> -o spec.yaml
   ```
6. Run Archerry with
   ```bash
   ./archerry/archerry spec.yaml
   ```

After installation a log file is created at `/var/log/archerry.log`.

Archerry creates shell scripts from your specification file and executes them
while showing a statusbar.

Created scripts are `main.bash`, `root.bash`, `user.bash` and are stored in
`archerry/dist` directory.

`main.bash` includes disk setup and pacstrap which should be run from iso. It
also includes chroot entries to `root.bash` and `user.bash`.

`root.bash` is run after pacstrap as root and includes bootloader setup and
user creation.

`user.bash` is run last as created user and includes most that's generated from
the specification file.

You can check installed files and packages with

```bash
archerry -c <FILE>
```

Example result:

```
Checking fs...
Different: /home/erm/.xinitrc
Missing: /etc/X11/xorg.conf.d/70-synaptics.conf
Total 5, Missing 1, Different 1

Checking pkg...
Missing: xf86-input-synaptics
Total 61, Missing 1
```

You can create & optionally run only the user script with

```bash
archerry -u <FILE>
```

See more with

```bash
archerry -h
```

## Related projects

- [Arch Installer](https://github.com/archlinux/archinstall)
  Official Arch Linux Installer
- [Decpac](https://github.com/rendaw/decpac)
  Arch Linux declarative package management
- [NixOS](https://nixos.org)
  Linux distribution based on the Nix package manager
