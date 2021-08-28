# Archerry 🌸

Declerative Arch Linux installer.

## Features

- [x] basic partitioning
- [x] base install (kernel, firmware, base, bootloader)
- [x] system setup from a specification file
- [x] incremental execution
- [ ] spec tag selection
- [ ] statistics
- [ ] custom iso

## Specification file

The system is configured with a YAML formatted specification/config file. Upon
execution user is prompted to fill missing fields in the specification and then
shell scripts are composed from the specification and run.

### Options

- `hostname` ‒ Hostname which is shown on the network
- `username` ‒ Username of the admin account
- `password` ‒ Password for the admin account
  > Not recommended to store in spec
- `timezone` ‒ Timezone keyword for
  [`timedatectl`](https://man.archlinux.org/man/timedatectl.1)
- `disk` ‒ Disk device path eg. `/dev/sda`
  > Not recommended to store in spec since it may not be consistent
- `swap` ‒ Swap size in MiB
- `yay` ‒ Whether to install and use `yay` for installing packages
- `pkg` ‒ Tree of packages
- `git` ‒ Tree of git repositories to clone
- `fs` ‒ Tree of files to write
- `cmd` ‒ Tree of commands to execute in the end

#### Example

Simple example of a specification file. See more at
[`example.archerry.yaml`](./example.archerry.yaml).

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
   clone https://gitlab.com/rasmusmerzin/archerry
   ```
5. Download your specification file with
   ```bash
   curl <URL> -o specification.yaml
   ```
6. Run Archerry with
   ```bash
   ./archerry/archerry specification.yaml
   ```

After installation a log file is created at `/var/log/archerry.log`.

Archerry creates shell scripts from your specification file and executes them
while showing a statusbar.

Created scripts are `main.bash`, `root.bash`, `user.bash` and are stored in
`archerry/dist` directory.

`main.bash` includes disk setup and pacstrap which should be run from iso. It
also includes chroot entries to `root.bash` and `user.bash`.

`root.bash` is run after pacstrap as root and includes bootloader setup, user
creation and currently locale & timezone setup.

`user.bash` is run last as created user and includes most that's created from
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
