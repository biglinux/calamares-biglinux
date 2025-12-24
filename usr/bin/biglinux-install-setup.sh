#!/bin/bash
#
# BigLinux Installation Setup Script
# Called by Calamares grubcfg-fix module after installation
#
# This script performs multiple post-installation setup tasks:
# 1. GRUB configuration (theme, kernel parameters, cleanup)
# 2. SDDM session configuration (Wayland/X11)
# 4. BigLinux live session config migration to installed system
#    (theme, desktop, JamesDSP audio, display profile)
#
# Usage: biglinux-install-setup.sh <root_mount_point>
# Example: biglinux-install-setup.sh /tmp/calamares-root-abc123
#

# Validate argument
ROOT_MOUNT="$1"
if [ -z "$ROOT_MOUNT" ] || [ ! -d "$ROOT_MOUNT" ]; then
    echo "Error: Invalid root mount point: $ROOT_MOUNT"
    exit 1
fi

# Define paths relative to root mount point
GRUB_FILE="$ROOT_MOUNT/etc/default/grub"
SDDM_STATE="$ROOT_MOUNT/var/lib/sddm/state.conf"
CONFIG_DIR="$ROOT_MOUNT/etc/big-default-config"

# Fix GRUB configuration
if [ -f "$GRUB_FILE" ]; then
    # Add kernel command line parameters from live session (cleaned)
    sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT='|GRUB_CMDLINE_LINUX_DEFAULT='$(sed 's|BOOT_IMAGE=/boot/vmlinuz-x86_64 ||g;s| driver=nonfree||g;s| driver=free||g;s| rdinit=/vtoy/vtoy||g;s| quiet splash||g' /proc/cmdline) |g" "$GRUB_FILE"

    # Remove live boot specific entries
    sed -i 's|BOOT_IMAGE=/boot/vmlinuz-x86_64||g;s|misobasedir=manjaro misolabel=BIGLINUXLIVE ||g' "$GRUB_FILE"

    # Set BigLinux GRUB theme
    sed -i 's|GRUB_THEME=.*|GRUB_THEME="/boot/grub/themes/biglinux/theme.txt"|g' "$GRUB_FILE"

    # Disable GRUB savedefault and fix duplicate quiet
    sed -i 's|GRUB_SAVEDEFAULT=true|GRUB_SAVEDEFAULT=false|g;s|quiet quiet|quiet|g' "$GRUB_FILE"

    # Add GRUB_EARLY_INITRD_LINUX_STOCK if not present
    if ! grep -q GRUB_EARLY_INITRD_LINUX_STOCK "$GRUB_FILE"; then
        echo "GRUB_EARLY_INITRD_LINUX_STOCK=''" >> "$GRUB_FILE"
    fi

    # Remove duplicate splash parameters
    while [ "$(grep -o '[^[:space:]]*splash[^[:space:]]*' "$GRUB_FILE" | sed 's/\"//' | wc -w)" -gt "1" ]; do
        sed -i 's/ splash//' "$GRUB_FILE"
    done

    # Remove duplicate quiet parameters
    while [ "$(grep -o '[^[:space:]]*quiet[^[:space:]]*' "$GRUB_FILE" | sed 's/\"//' | wc -w)" -gt "1" ]; do
        sed -i 's/ quiet//' "$GRUB_FILE"
    done
fi

# Configure SDDM session based on boot mode
mkdir -p "$(dirname "$SDDM_STATE")"
if grep -q wayland /proc/cmdline; then
    echo "[Last]
    Session=/usr/share/wayland-sessions/plasmawayland.desktop" > "$SDDM_STATE"
else
    echo "[Last]
    Session=/usr/share/xsessions/plasma.desktop" > "$SDDM_STATE"
fi

# Copy BigLinux configuration files from /tmp to installed system
# During live session, biglinux-livecd saves configs to /tmp
mkdir -p "$CONFIG_DIR"

# Copy theme config if exists
[ -f "/tmp/big_desktop_theme" ] && cp -f "/tmp/big_desktop_theme" "$CONFIG_DIR/theme"

# Copy desktop config if exists
[ -f "/tmp/big_desktop_changed" ] && cp -f "/tmp/big_desktop_changed" "$CONFIG_DIR/desktop"

# Copy JamesDSP flag if exists
[ -f "/tmp/big_enable_jamesdsp" ] && cp -f "/tmp/big_enable_jamesdsp" "$CONFIG_DIR/jamesdsp"

# Copy display profile flag if exists
[ -f "/tmp/big_improve_display" ] && cp -f "/tmp/big_improve_display" "$CONFIG_DIR/display-profile"

echo "BigLinux installation setup completed successfully"
