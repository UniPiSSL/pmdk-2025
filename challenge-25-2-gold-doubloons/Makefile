default: print
	tar cvf dist/docker-challenge.tar -C src app Dockerfile flag.txt
	cd src/app/ && zip -r - . --exclude='*flag*' > ../../dist/misc-2-gold-doublons.zip
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	rm -f dist/docker-challenge.tar
	rm -f dist/misc-2-gold-doublons.zip
	@echo Challenge cleaned.
