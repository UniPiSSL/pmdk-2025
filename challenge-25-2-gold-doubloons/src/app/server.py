# Awwwww no flag? :'( 
whitelist = "e.d',no)p(a%rcl"
 
# Awwww input sanitization :'( 
Anti_Cheating = lambda check: any(c not in whitelist for c in check)

# Awww spongebob reference :'( 
def Magic_Conch_shell():
	Ev4l_m3_pL3a5e = input("Oh magic conch shell > ")
	if Anti_Cheating(Ev4l_m3_pL3a5e):
		print('Th3 Sh3ll h45 Sp0k3n: Nothing!')
		exit()
	print(f'Th3 Sh3ll h45 Sp0k3n: {eval(Ev4l_m3_pL3a5e)}')

while True:
	Magic_Conch_shell()
