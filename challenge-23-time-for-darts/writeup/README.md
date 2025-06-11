# Time for Darts Write-Up

| Δοκιμασία | Time for Darts |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία | Διάφορα (Miscellaneous) |
| Λύσεις | 14 |
| Πόντοι | 389 |


## Περιγραφή Δοκιμασίας

``` 
Ένας διαγωνισμός ξεκινάει... Μπορείς να κρατάς την βαθμολογία;
```

## Επίλυση

Όπως φαίνεται και από την περιγραφή, για να πάρουμε την σημαία θα πρέπει να γράψουμε ένα bot το οποίο θα κρατάει την βαθμολογία.

Το script θα πρέπει να είναι αυτοματοποιημένο και να συνδέεται στον διακομιστή μέσω TCP (μπορούμε να κάνουμε χρήση της βιβλιοθήκης pwntools). Επιπλέον, θα πρέπει να κάνει ανάλυση σκορ των παικτών και να εντοπίζει τον νικητή κάθε γύρου.

Ενδεικτικά δίνεται ένα τέτοιο scipt:

```
#!/usr/bin/env python3
import time
import sys
import argparse
from pwn import *

# Example run:
# python3 solution.py challenges.example.com 1337 --debug

parser = argparse.ArgumentParser(description="Netcat Whisperer", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug log level")
parser.add_argument("-w", "--wait", type=int, help="Seconds to wait for process to start")
parser.add_argument("target", help="Server's IP, Domain Name or Shell Command")
parser.add_argument("port", help="Server's Port", type=int, nargs='?', default=0)
args = parser.parse_args()
config = vars(args)


# Check log level
if config['debug']:
	context.log_level = "debug"

print('Connecting ...')

try:
	if not (1 <= config['port'] and config['port'] <= 65536):
		raise ValueError('Invalid port number.')
	p = remote(config['target'], config['port'])
	#p = process('python3 ../src/app/service.py', shell=True)

# Handle errors
except Exception as e:
	raise(e)
	print('[E] Failed to etablish a connection.')
	print(e)
	sys.exit(1)

# Wait after connection
if config['wait']:
	time.sleep(config['wait'])

# Get nuber of players
catchPlayersPhrase = "players!!"
ret = p.recvuntil(catchPlayersPhrase.encode()).decode("utf-8") # Wait for server's message end
response = ret.split("\n")
playerNr = response[-1].split(" ")[-2]
print('Number of players: ', playerNr)

# Pass server's welcome message
server_header_end = b"> "
ret = p.recvuntil(server_header_end).decode("utf-8") # Wait for server's message end

# If the challenge has a menu, you may want to send here an input to that menu
answer = '1'
p.sendline(answer.encode())

# Start main loop to process a challenge's stages
ret = None

# Wait for stage's information
#	Your answer: 
try:
	ret = p.recvuntil(b"> ",  timeout=200).decode("utf-8")
except Exception as e:
	print('[E] Failed recover stage. Wrong answer?')

# Solve the given problem here using the information extracted
response = ret.split("\n")[7::]
#print(response)
rounds = 40
playerScores = {}

for player in range(int(playerNr)):
	playerScores[player] = 0
for round in range(rounds):
	for player in range(int(playerNr)):
		print(f"Round {round}")
		lineWanted = response[round*int(playerNr) + round + player + 1]
		playerScores[player] += int(lineWanted.split(" ")[-2])

correctPlayer = [key for key, value in playerScores.items() if value == max(playerScores.values())]
winningPlayer = sorted(correctPlayer)[0] + 1
correctScore = max(playerScores.values())
print("Winner is " + str(winningPlayer) + " with a score of " + str(correctScore))

# Send your answer to the server
answer = "Player " + str(winningPlayer)
p.sendline(answer.encode())

try:
	ret = p.recvuntil(b"> ",  timeout=5).decode("utf-8")
except Exception as e:
	print('[E] Failed recover stage. Wrong answer?')

time.sleep(0.2)

# Send your answer to the server
answer = str(correctScore)
p.sendline(answer.encode())


# Pass the session back to the user
# By doing so, the output of the server is passed to the user console
# so that we dont miss the flag
p.interactive()
```

Το script κάνει τις παρακάτω ενέργειες για να καταφέρει να πάρει το flag:

 - Διαβάζει δεδομένα που περιγράφουν πόντους για 40 γύρους
 - Υπολογίζει το σύνολο των πόντων για κάθε παίκτη
 - Βρίσκει τον παίκτη με το μεγαλύτερο σκορ (νικητής)
 - Στέλνει το όνομα του νικητή, π.χ., `"Player 2"`
 - Στέλνει το συνολικό σκορ του νικητή, π.χ., `"1234"`
