#!/bin/bash

echo Update the password for the current user
passwd

CURRENT_HOSTNAME=`cat /etc/hostname | tr -d " \t\n\r"`
if [ "$INTERACTIVE" = True ]; then
  NEW_HOSTNAME=$(whiptail --inputbox "Please enter a hostname" 20 60 "$CURRENT_HOSTNAME" 3>&1 1>&2 2>&3)
else
  NEW_HOSTNAME=$1
  true
fi
if [ $? -eq 0 ]; then
  echo $NEW_HOSTNAME > /etc/hostname
  sed -i "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$NEW_HOSTNAME/g" /etc/hosts
fi

apt-get update

raspi-config --expand-rootfs
