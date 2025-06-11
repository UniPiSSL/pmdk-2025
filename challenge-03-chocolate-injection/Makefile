default: print
	tar cvf dist/docker-challenge.tar -C src html config Dockerfile flag.txt
	cd src && zip -r - . --exclude='*flag*' > ../dist/web-chocolate-injection.zip
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	rm -f dist/docker-challenge.tar
	rm -f dist/web-chocolate-injection.zip
	@echo Challenge cleaned.
