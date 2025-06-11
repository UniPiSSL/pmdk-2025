#!/bin/bash

# Init server
bash /tmp/setup.sh
rm -f /tmp/setup.sh

# Start SSH server
/usr/sbin/sshd -D
