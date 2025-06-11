default: print
	cd src/app && node ./generate.js
	cd src/app && zip -r - . --exclude='flag.txt' --exclude='generate.js' > ../nwbin.nw
	cd src && rm -rf ./nwbin
	cd src && mkdir -p ./nwbin && cat ./nw.exe ./nwbin.nw > ./nwbin/nwbin.exe
	# split -b 50M nwjs-files.zip nwjs-files-part-
	cd src && cat nwjs-files-part-* > nwjs-files.zip
	rm -rf ./dist/rev-nwbin.zip
	mv ./src/nwjs-files.zip ./dist/rev-nwbin.zip
	cd src && zip -r ../dist/rev-nwbin.zip nwbin
	cd src && rm -rf ./nwbin && rm -rf nwbin.nw
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/app/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/app/flag.txt')
	@echo Flag changed.

clean:
	rm -f src/nwbin.nw
	rm -f dist/rev-nwbin.zip
	@echo Challenge cleaned.
