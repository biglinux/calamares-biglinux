#!/bin/bash

#sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT=\"|GRUB_CMDLINE_LINUX_DEFAULT=\"$(cat /proc/cmdline | sed 's|.*misolabel=[[:alnum:]_-]*||g;s|bootsplash.bootfile=[[:alnum:]/_-]*||g;s|quiet systemd.show_status=1||g;s|driver=nonfree||g;s|driver=free||g;s|nouveau.modeset=0 i915.modeset=1 radeon.modeset=1||g;s|nouveau.modeset=1 i915.modeset=1 radeon.modeset=1||g')|g" $*


sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT=\"|GRUB_CMDLINE_LINUX_DEFAULT=\"$(sed 's|BOOT_IMAGE=/boot/vmlinuz-x86_64 ||g;s| driver=nonfree||g;s| driver=free||g;s| rdinit=/vtoy/vtoy||g;s| quiet splash||g' /proc/cmdline) |g" $*

sed -i 's|BOOT_IMAGE=/boot/vmlinuz-x86_64||g;s|misobasedir=manjaro misolabel=BIGLINUXLIVE ||g' $*

sed -i 's|GRUB_THEME=.*|GRUB_THEME="/boot/grub/themes/biglinux/theme.txt"|g' $*

sed -i 's|GRUB_SAVEDEFAULT=true|GRUB_SAVEDEFAULT=false|g;s|quiet quiet|quiet|g' $*

#remove multiples splash
while [ "$(grep -o '[^[:space:]]*splash[^[:space:]]*' $* | sed 's/\"//' | wc -w)" -gt "1" ];do
    sed -i 's/ splash//' $*
done
#remove multiples quiet
while [ "$(grep -o '[^[:space:]]*quiet[^[:space:]]*' $* | sed 's/\"//' | wc -w)" -gt "1" ];do
    sed -i 's/ quiet//' $*
done

#Change default desktop in sddm to use in livecd
echo "[Last]
Session=/usr/share/xsessions/plasma-biglinux-x11.desktop" > $(echo "$*" | sed 's|etc/default/grub|var/lib/sddm/state.conf|g')

sed -i "s|Session=plasma.desktop|Session=plasma-biglinux-x11.desktop|g" $(echo "$*" | sed 's|etc/default/grub|etc/sddm.conf|g')

# use compress-force=zstd:5 in /git 
sed -i 's|subvol=/@,defaults,noatime,compress=zstd|subvol=/@,defaults,noatime,compress-force=zstd:5|g' $(echo "$*" | sed 's|etc/default/grub|/etc/fstab|g')

# Save default KDE configuration

cp -f "/etc/big_desktop_changed" $(echo "$*" | sed 's|etc/default/grub|/etc/big_desktop_changed|g')

# if [ -e "/tmp/use_disable_fsync" ]; then
#     echo '/usr/$LIB/disable-fsync.so' > $(echo "$*" | sed 's|etc/default/grub|etc/ld.so.preload|g')
# fi


cp -f /tmp/big_desktop_theme $(echo "$*" | sed 's|etc/default/grub|etc/default-theme-biglinux|g')
