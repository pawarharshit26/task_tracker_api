.PHONY: fmt

SRC := app

fmt:
	black $(SRC)
	ruff check $(SRC) --fix