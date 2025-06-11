import os
import random
import argparse
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from moviepy.editor import AudioFileClip, VideoClip

# Morse Code Dictionary
MORSE_CODE_DICT = {
	'A': '.-',    'B': '-...',  'C': '-.-.', 'D': '-..',  'E': '.',    
	'F': '..-.',  'G': '--.',   'H': '....', 'I': '..',   'J': '.---', 
	'K': '-.-',   'L': '.-..',  'M': '--',   'N': '-.',   'O': '---',  
	'P': '.--.',  'Q': '--.-',  'R': '.-.',  'S': '...',  'T': '-',    
	'U': '..-',   'V': '...-',  'W': '.--',  'X': '-..-', 'Y': '-.--', 
	'Z': '--..',
	'1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
	'6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
	' ': '  '  # Two spaces to separate words
}

# Function to convert text to Morse code
def text_to_morse(text):
	morse_code = ''
	for char in text.upper():
		if char in MORSE_CODE_DICT:
			morse_code += MORSE_CODE_DICT[char] + ' '  # Add space after each letter
		elif char == ' ':
			morse_code += '  '  # Space means 2 spaces
		else:
			print(f"Warning: Character '{char}' cannot be encoded in Morse.")
	return morse_code.strip()

# Function to convert Morse code to an audio file
def code_to_audio(morse_code, output_file="code.mp3"):
	dot_duration = 100  # milliseconds
	dash_duration = 300
	freq = 800  # Hz, the tone frequency
	pause_duration = 100  # Pause between dots/dashes
	extended_duration = 1000  # Longer pause between words
	dtmf_freq = {
		'1': (697, 1209),
		'2': (697, 1336),
		'3': (697, 1477),
		'4': (770, 1209),
		'5': (770, 1336),
		'6': (770, 1477),
		'7': (852, 1209),
		'8': (852, 1336),
		'9': (852, 1477),
		'*': (941, 1209),
		'0': (941, 1336),
		'#': (941, 1477),
	}

	dot = Sine(freq).to_audio_segment(duration=dot_duration)
	dash = Sine(freq).to_audio_segment(duration=dash_duration)
	pause = AudioSegment.silent(duration=pause_duration)
	extended_pause = AudioSegment.silent(duration=extended_duration)

	audio = AudioSegment.silent(duration=0)  # Start with empty audio segment

	for symbol in morse_code:
		if symbol == '.':
			audio += dot + pause
		elif symbol == '-':
			audio += dash + pause
		elif symbol == ' ':
			audio += extended_pause
		elif symbol in dtmf_freq:
			duration = random.randint(dot_duration, dash_duration)
			low_freq, high_freq = dtmf_freq[symbol]
			tone_low = Sine(low_freq).to_audio_segment(duration=duration)
			tone_high = Sine(high_freq).to_audio_segment(duration=duration)
			audio += tone_low.overlay(tone_high) + pause
		else:
			pass  # Ignore invalid symbols

	audio.export(output_file, format="mp3")
	print(f"MP3 file saved as {output_file}")

# Function to generate a waveform visualizer video
def generate_visualizer(audio_file, output_video="morse_visualizer.mp4"):
	audio_clip = AudioFileClip(audio_file)
	duration = audio_clip.duration

	video_width = 1280
	video_height = 720
	video_half_height = int(video_height / 2)
	pulse_height = int(video_height / 3)

	# Function to draw waveform frames
	def make_waveform_frame(t):
		"""Generates a single frame for the waveform visualization."""
		samples = audio_clip.to_soundarray(fps=44100)  # Extract samples
		start_index = int(t * 44100)
		end_index = min(start_index + 441, len(samples))  # 10ms worth of samples
		waveform = samples[start_index:end_index]
		waveform = np.mean(waveform, axis=1)  # Average stereo to mono

		# Normalize and scale the waveform
		waveform = (waveform - waveform.min()) / (waveform.max() - waveform.min())
		waveform = (waveform * pulse_height).astype(int)

		# Draw the waveform as a white line
		frame = np.zeros((720, video_width, 3), dtype=np.uint8)  # Black frame
		for i, y in enumerate(waveform):
			x = int(i * video_width / len(waveform))  # Map sample index to frame width
			frame[video_half_height - y:video_half_height + y, x] = (255, 255, 255)  # Draw symmetrical white line
		return frame

	# Generate video clip with waveform frames
	waveform_clip = VideoClip(make_waveform_frame, duration=duration)
	waveform_clip = waveform_clip.set_audio(audio_clip)
	waveform_clip.write_videofile(output_video, fps=60, codec="libx264", audio_codec="aac")
	print(f"Video saved as {output_video}")


# Load flag from file if exists
flag = 'CTFLIB{example-flag}'
if os.path.isfile('flag.txt'):
	with open('flag.txt', 'r') as f:
		flag = f.read().strip()

# From the flag, remove prefix and suffix (we can not have "{" or "}" in morse)
flag_content = flag.split('{', 1)[1]
flag_content = flag_content.rsplit('}', 1)[0]

# Contents to encode:
code = ""
for c in flag_content:
	if not c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789*0#':
		print(f'Warning! Character {c} will be ignored.')
	else:
		code += c
print(f"Contents to encode: {code}")

# Encode in morse
code = text_to_morse(code)
code = " " + code + " " # Add extra pause infront and back

# Convert to audio
print("Generating audio...")
code_to_audio(code, "code.mp3")

# Convert to video
print("Generating video...")
generate_visualizer("code.mp3", "code.mp4")


'''
# Main function to parse arguments and run the pipeline
def main():
	parser = argparse.ArgumentParser(description="Convert text to Morse code, generate sound, and create a visualizer video.")
	parser.add_argument("text", type=str, help="The text string to encode into Morse code.")
	parser.add_argument("--audio", type=str, default="morse_code.mp3", help="Output filename for the Morse code audio.")
	parser.add_argument("--video", type=str, default="morse_visualizer.mp4", help="Output filename for the visualizer video.")

	args = parser.parse_args()

	# Step 1: Convert text to Morse code
	print("Converting text to Morse code...")
	morse_code = text_to_morse(args.text)
	print("Morse Code:", morse_code)

	# Add extra pause infront and back
	morse_code = " " + morse_code + " "

	# Step 2: Generate audio file
	print("Generating Morse code audio...")
	code_to_audio(morse_code, args.audio)

	# Step 3: Generate visualizer video
	print("Generating visualizer video...")
	generate_visualizer(args.audio, args.video)

	print("Process completed successfully!")

if __name__ == "__main__":
	main()
'''
