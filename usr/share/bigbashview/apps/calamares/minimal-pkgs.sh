#!/bin/bash

# Read minimal-pkgs.txt and verify that each package is installed
# And output json file to be used by bigbashview

# Save the list of installed packages to a file
pacman -Qq > /tmp/big-installed-packages.txt

# Load the icon mappings from the icon-mapping.txt file
declare -A icon_map
while IFS=' ' read -r package icon; do
    icon_map[$package]=$icon
done < icon-mapping.txt

# Get the icons for the packages in the minimal-pkgs.txt file
# and use column to display the results as json
(for i in $(grep -Fxf minimal-pkgs.txt /tmp/big-installed-packages.txt); do
    icon=${icon_map[$i]:-$i}
    echo "$i $(geticons -s 48 $icon)"
done) | column --table-name packages --table-columns pkg,icon -J
