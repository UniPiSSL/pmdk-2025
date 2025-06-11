#!/usr/bin/env python3
import random
import time
import sys
import numpy as np

# Challenge Variables
# -----------------------------------------------------------

game_rounds		= 40
player_nr		= random.randint(5, 15)
starting_score	= 0
timeout 		= 1

# Possible scores based on dartboard layout
single_sections = list(range(1, 21))  # Sections 1 to 20 (single)
double_sections = [2*x for x in range(1, 21)]	# Double sections
triple_sections = [3*x for x in range(1, 21)]	# Triple sections
bullseye = [50, 25, 0] 							# Inner & outer bullseye // miss

# Combine all possible scores
possible_scores = single_sections + double_sections + triple_sections + bullseye

# Simulation parameters
num_throws = 100000  # Number of dart throws for simulation

# Simulate throws
throws = np.random.choice(possible_scores, size=num_throws, replace=True)

# Calculate the frequency of each score
score_counts = np.bincount(throws, minlength=61)  # Scores range from 0 to 60

# Normalize to get the probability of each score
probabilities = score_counts / num_throws
# Game setup: Start at 0 points
player_score = {}
for player in range(player_nr):
	player_score[player] = 0

# Action Handler
# -----------------------------------------------------------

def userinput(question, correct_answer):
	# Show question
	print(question)
	# Get user response
	given_answer = input("> ")
	# Check answer
	return (str(correct_answer) == given_answer.strip())

# Game loop
def throw_dart():
	return np.random.choice(range(61), p=probabilities)

# Rounds loop Function
# -----------------------------------------------------------
# Simulate a game of darts
def play_darts_game(rounds, player_nr):
	print("")
	for round in range(rounds):
		print(f"---------   Results of round {round + 1}   ---------")
		for player in range(player_nr):
			# Throw a dart
			score = throw_dart()
			# Subtract score from player"s total
			player_score[player] += score
			time.sleep(0.1)
			print(f"Player {player + 1}: Scored {score} points.")
			# Print to check it manually
			#print(f"Player {player + 1 }: Scored {score} points. Total score: {player_score[player]}")
	
	winningPlayers = [key for key, value in player_score.items() if value == max(player_score.values())]
	winningPlayer = str(sorted(winningPlayers)[0] + 1)
	winningScore = str(max(player_score.values()))
	#print(f"Who is the winner of this game? Winner: {winningPlayer} with {winningScore}")
	print("Who is the winner of this game?")
	time.sleep(0.05)
	start = time.time()
	answerPlayer = input("> ").lower()
	print("What was the highest score?")
	time.sleep(0.05)
	answerScore = input("> ")
	if time.time() - start > timeout:
		print("Oh no... You were too late.. Unfortunately no winner was announced for this game..")
		return False

	if not answerPlayer.startswith('player '):
		print("What is that? The player input does not have the format I told you...")
		return False

	if not answerScore.isdigit():
		print("What is that? The score input is not a number...")
		return False

	if (answerPlayer != f"player {winningPlayer}") or answerScore != winningScore:
		print("Oops.. Your machine cannot keep track of the correct score..")
		return False

	print("Wow!! You are so quick and accurate! Congrats!")
	return True

# Challenge Start
# -----------------------------------------------------------

print("WE WELCOME YOU TO THE FIRST .... \033[1;31me-DART\033[0m GAME OF \033[1;34mPMDK\033[0m")
print("*shouting* *coughing* *talking* *drinking*")
print("                        ___")
print("                      /\\ _ /\\")
print("    >>>----          / /\\ /\\ \\")
print(">>>----             |---(*)---|")
print("                     \\ \\/_\\/ /")
print("         >>>----      \\/___\\/")
print("")
time.sleep(0.3)
print(f"Hello, I am sorry but player registrations closed just one minute ago! We already have {player_nr} players!!")
time.sleep(0.2)
print("Oh, no wait! I might have an empty spot for you my dear friend.")
time.sleep(0.1)
print("Our scorekeeper is not here yet and the game is about to start.")
time.sleep(0.1)
print("Can you help us? Do you maybe have a calculator on you?")
time.sleep(0.1)
print("A, what? A computer? Oh, ok you can try, but you have to be fast, because these players are proffessionals. Will you be able to keep track?")
print("")

time.sleep(0.5)
print("Ok ok I hear you! You can keep the score with your little machine!")
time.sleep(0.2)
print("I\'ll quickly go over the rules of the game...")
time.sleep(0.5)
print(f"1. Each game consists of {game_rounds} rounds.")
time.sleep(0.2)
print("2. Each player shoots only one dart each round. The score of each shot will be shown to you.")
time.sleep(0.2)
print("3. Each round's score is added to the player\'s overall score.")
time.sleep(0.5)
print("4. At the end of the game the player with the highest overall score is the winner (i.e. \"Player 3\").")
time.sleep(0.5)
print("5. In case of draw, the player who played first is the winner.")
time.sleep(1) 
print("Do you have any questions?")
time.sleep(0.5)
print("*chirping*")
time.sleep(0.5)
print("No? Ok good!")
time.sleep(0.5)
print("")

time.sleep(0.5)
print("Now... Prepare your fancy calculator, they are about to start ...")
time.sleep(0.5)
print("*shouting* *coughing* *talking* *drinking*")
time.sleep(0.5)
print("Everyone please be quite.. The game is starting...")
print("Are you ready?")
print("1. Yes")
print("2. No")
if not input("> ").strip() == "1":
	print("Oh well... I\'ll find another one..")
	sys.exit()

print("")

# Start game
print("")
time.sleep(0.5)
print("3 ...")
time.sleep(0.5)
print("2 ...")
time.sleep(0.5)
print("1 ...")
time.sleep(0.5)
print("Go!")

if not play_darts_game(game_rounds, player_nr):
	print("Can you format this thing and come back next year please???")
	sys.exit()

# Challenge Completed
# -----------------------------------------------------------

time.sleep(0.2)
print("")
print("")
print("Nice job!")
time.sleep(0.2)

print("Thank you very much for your help kind sir!")
time.sleep(0.2)
print("Oh, I almost forgot... Before you go here is your reward!!")
time.sleep(0.5)
with open("flag.txt") as f:
	flag = f.read().strip()
print(flag)
print("")
