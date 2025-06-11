default:
	cd src && python3 source.py && cp output.txt ../writeup
	cd src && zip -r --exclude='*secret*' ../dist/crypto-best-wishes.zip .
	@echo Challenge compiled.

solve:
	@cd writeup && python3 solver.py

clean:
	rm -f dist/*
	@echo Challenge cleaned.

