#!/bin/bash

set +xe

# check command
if [ "$*" != "" ]
then
  mason_command=$*
else
  echo "ERROR: Nothing to execute!"
  exit 1
fi

## setup services for bluetooth
echo "Setup Bluetooth environment inside docker..."
sudo service dbus start || echo "desktop bus didn't start"
sudo bluetoothd &
# TODO: Here you can add your needed setups

## Prepare for Appium usage, add config file for test user
mkdir -p /home/${HOST_USER}/.appium/node_modules/.cache/appium
chown ${HOST_USER} /home/${HOST_USER}/.appium -R
cp /usr/lib/node_modules/appium/extensions.yaml /home/${HOST_USER}/.appium/node_modules/.cache/appium

## execute mason
echo "Setup done, execute tests"
$mason_command
mason_exitcode=$?
echo "Mason test framework returned exit code: $mason_exitcode"

## teardown services for bluetooth
sudo kill $(pidof bluetoothd)
sudo service dbus stop || echo "failed to stop desktop bus"
# TODO: Here you can add your needed teardowns

exit $mason_exitcode
