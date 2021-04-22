#!/bin/bash

sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT=\"|GRUB_CMDLINE_LINUX_DEFAULT=\"$(cat /proc/cmdline | sed 's|initrd=.*||g;s|.*union=overlay||g;s|toram||g;s|quiet||g;s|splash||g;s|.*driver=free ||g;s|misobasedir=manjaro ||g;s|misolabel=M1804 ||g')|g" $*



sed -i "s|security=apparmor ||g;s|apparmor1 ||g;s|udev.log_priority=3||g;s|quiet| quiet splash |g')|g" $*

sed -i 's|GRUB_THEME=.*|GRUB_THEME=/boot/grub/themes/biglinux/theme.txt|g' $*

sed -i 's|GRUB_SAVEDEFAULT=true|GRUB_SAVEDEFAULT=false|g' $*





#Change default desktop in sddm to use in livecd
echo "[Last]
Session=$(cat /tmp/big_desktop_changed)" > $(echo "$*" | sed 's|etc/default/grub|var/lib/sddm/state.conf|g')

cp -f /tmp/big_desktop_theme $(echo "$*" | sed 's|etc/default/grub|etc/default-theme-biglinux|g')
