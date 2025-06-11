pack:
	@mkdir -p dist/emojious && cp src/emojious.py dist/emojious
	@cd dist && zip -9 -r - emojious > rev-emojious.zip
	@cd dist && rm -rf emojious
	@echo Challenge packed.

clean:
	@rm -rf dist/*
