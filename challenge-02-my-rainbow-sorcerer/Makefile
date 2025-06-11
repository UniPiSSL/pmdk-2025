default:
	cd src/app && zip -r - . --exclude='**flag**' --exclude='**requirements**'> ../../dist/crypto-my-rainbow-sorcerer.zip
	tar cvf dist/docker-challenge.tar -C src Dockerfile app
	@echo Challenge Compiled.

print:
	@echo Current Flag: $$(cat src/app/flag.txt)

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/app/flag.txt')
	@echo Flag changed.


change:  print changeflag clean default print

clean:
	rm -f dist/docker-challenge.tar
	rm -f dist/crypto-my-rainbow-sorcerer.zip
	@echo Challenge cleaned.
