#!/bin/bash

## PYMAILER INSTALLER SCRIPT
##
## Run this script as root in order to install the pymailer system.


# Constants
BIN_DIR="/usr/local/bin"
CNF_DIR="/etc"
LOG_DIR="/tmp"
BASE_VER="v.1.1-GH"

BIN_PATH=$BIN_DIR/pymailer
CNF_PATH=$CNF_DIR/pymailer.conf
LOG_PATH=$LOG_DIR/pymailer.log

# Check if running with root privileges
if [ $EUID -ne 0 ]; then
    echo -e "\n  Insufficient Privileges!"
    echo -e "Must run as root or use sudo!\n"
    exit
fi

# Install dependencies - right now I'm mainly targeting Debian-based systems, 
apt install -y python3 git

# Make sure the repo is in the "safe directory" list for your user
git config --global --add safe.directory /home/chip/gitWD/pymailer

# Copy files and set permissions
cp ./pymailer.py $BIN_PATH
cp ./pymailer.conf $CNF_PATH
chmod +x $BIN_PATH

echo -e "\n\nFiles have been installed - now it's time to configure PyMailer!\n"
read -p "What is the username (email address) that PyMailer will use to send? " username
read -sp "Cool. And what is the password for that account? (characters you type won't show on screen) " pass
echo
read -p "Awesome! When PyMailer sends emails, what do you want the default 'Subject' line to be? " subject
read -p "Lastly, which email address do you want PyMailer to send to when you don't specifiy a recipient? " sendTo

echo -e "\nI have what I need - configuring PyMailer now..."
commitNum="$(git rev-parse --short HEAD)"
vers="$BASE_VER-$commitNum"

sed -i "s/__USERNAME__/$username/g" $CNF_PATH  # Some of the sed lines use
sed -i "s|__PASSWORD__|$pass|g" $CNF_PATH      # pipes (|) because the text
sed -i "s/__SUBJECT__/$subject/g" $CNF_PATH    # they're working with might
sed -i "s/__SENDTO__/$sendTo/g" $CNF_PATH      # have slashes in it. 
sed -i "s|__LOGFILE__|$LOG_PATH|g" $CNF_PATH
sed -i "s/__VERSION__/$vers/g" $CNF_PATH
sed -i "s|__CONF__|$CNF_PATH|g" $BIN_PATH

echo -e "\nPyMailer is now fully installed. If you need to make any further changes, the"
echo -e "config file is located at $CNF_PATH.\n\n"
