.PHONY: lint fmt run dev


# Lint code (check only)
lint:
	@ruff check app

# Format code (auto-fix)
fmt:
	@ruff check app --fix
	@ruff format app

# Run server
run:
	@uvicorn app.main:app --reload --port 8001

# Shortcut for dev workflow: format + run
dev: 
	@fmt run