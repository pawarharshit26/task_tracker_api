.PHONY: fmt

SRC := app

fmt:
	black $(SRC)
	ruff check $(SRC) --fix

migrate:
	alembic -c app/alembic.ini upgrade