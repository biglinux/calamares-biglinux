#!/bin/bash

#sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT=\"|GRUB_CMDLINE_LINUX_DEFAULT=\"$(cat /proc/cmdline | sed 's|.*misolabel=[[:alnum:]_-]*||g;s|bootsplash.bootfile=[[:alnum:]/_-]*||g;s|quiet systemd.show_status=1||g;s|driver=nonfree||g;s|driver=free||g;s|nouveau.modeset=0 i915.modeset=1 radeon.modeset=1||g;s|nouveau.modeset=1 i915.modeset=1 radeon.modeset=1||g')|g" $*

cat /proc/cmdline | sed 's|.*misolabel=[[:alnum:]_-]*||g;s|driver=nonfree||g;s|driver=free||g'

sed 's|  *| |g' $*

sed -i 's|GRUB_THEME=.*|GRUB_THEME="/boot/grub/themes/biglinux/theme.txt"|g' $*

sed -i 's|GRUB_SAVEDEFAULT=true|GRUB_SAVEDEFAULT=false|g' $*





#Change default desktop in sddm to use in livecd
echo "[Last]
Session=$(cat /tmp/big_desktop_changed)" > $(echo "$*" | sed 's|etc/default/grub|var/lib/sddm/state.conf|g')



if [ -e "/tmp/use_disable_fsync" ]; then
    echo "/usr/lib/disable-fsync.so" > $(echo "$*" | sed 's|etc/default/grub|etc/ld.so.preload|g')
fi


cp -f /tmp/big_desktop_theme $(echo "$*" | sed 's|etc/default/grub|etc/default-theme-biglinux|g')
