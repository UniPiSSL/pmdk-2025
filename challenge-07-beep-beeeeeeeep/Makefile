SHELL := /bin/bash

default: print
	cd src && zip -r - social_image.png > ../dist/misc-beep-beeeeeeeep.zip
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	#$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	#@echo Flag changed.
	@echo Flag change has been disabled.

clean:
	rm -f dist/misc-beep-beeeeeeeep.zip
	@echo Challenge cleaned.
