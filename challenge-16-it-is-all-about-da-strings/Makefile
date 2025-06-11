default: print
	cd src/ && gcc -O0 binary.c -o binary
	cd src/ && zip -r ../dist/rev-it-is-all-about-da-strings.zip binary
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	rm -f dist/rev-it-is-all-about-da-strings.zip
	@echo Challenge cleaned.
