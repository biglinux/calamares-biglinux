#!/bin/bash

sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT=\"|GRUB_CMDLINE_LINUX_DEFAULT=\"$(cat /proc/cmdline | sed 's|initrd=.*||g;s|.*union=overlay||g;s|toram||g;s|quiet||g;s|splash||g')|g" $*

echo 'GRUB_THEME=/boot/grub/themes/biglinux/theme.txt' >>  $*


#Change default desktop in sddm to use in livecd
echo "[Last]
Session=$(cat /tmp/big_desktop_changed)" > $(echo "$*" | sed 's|etc/default/grub|var/lib/sddm/state.conf|g')

cp -f /tmp/big_desktop_theme $(echo "$*" | sed 's|etc/default/grub|etc/default-theme-biglinux|g')
