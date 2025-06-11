default: print
	tar cvf dist/docker-challenge.tar -C src files Dockerfile
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/files/documents/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/files/documents/flag.txt')
	@echo Flag changed.

clean:
	rm -f dist/docker-challenge.tar
	@echo Challenge cleaned.
