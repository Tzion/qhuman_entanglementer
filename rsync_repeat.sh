#!/bin/bash

directory="$(basename "$(dirname "$(readlink -f "$0")")")"

if [ $# -eq 2 ]; then
    username=$1
    ip=$2
else
    read -p "Enter the username (for SSH session): " username
    read -p "Enter the remote IP address: " ip
fi
destination=$username@$ip:'~/'
echo "Syncing '$directory' directory to $destination"
fswatch -o "$directory" | while read f; do
    rsync -avz  --exclude='*env*' --exclude='*/__pycache__/' --exclude='*/.vscode/' --include='*/' --include='*.py' --include='*.ino' --include='*.sh' --include='*.mp3'  -e ssh "$directory" "$destination"
done