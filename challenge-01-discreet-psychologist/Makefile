default:
	cd src/ && zip -r - source.py output.txt --exclude='*flag*' > ../dist/crypto-discreet-psychologist.zip
	cp src/output.txt writeup/
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.


change:  print changeflag clean default print

clean:
	rm -f src/output.txt
	rm -f writeup/output.txt
	rm -f dist/crypto-discreet-psychologist.zip
	@echo Challenge cleaned.
