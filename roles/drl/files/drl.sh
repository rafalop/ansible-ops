#!/bin/bash
# a crude script to force through do-release-upgrades

nohup do-release-upgrade -f DistUpgradeViewNonInteractive </dev/null >/dev/null 2>&1 &

drl_pid=$!

sleep 270

while $(kill -0 $drl_pid); do
  dpkg_pid=$(ps -C dpkg -o pid --no-headers)
  touch "/proc/${dpkg_pid}/fd/0"
  sleep 30
done
