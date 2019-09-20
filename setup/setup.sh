#!/bin/bash

echo Update the password for the current user
passwd

CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
NEW_HOSTNAME=$(whiptail --inputbox "Please enter a hostname" 20 60 "$CURRENT_HOSTNAME" 3>&1 1>&2 2>&3)
if [ $? -eq 0 ]; then
  echo $NEW_HOSTNAME | sudo tee /etc/hostname
  sudo sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts
fi

sudo apt-get update
sudo apt-get --yes install git

git clone https://github.com/secretheadquarters/pager.git

sudo raspi-config --expand-rootfs

whiptail --msgbox "Now please reboot the system" 20 60 2
