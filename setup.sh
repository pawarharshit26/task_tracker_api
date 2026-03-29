#!/bin/bash

# setup.sh - Environment setup script for pragya_api (uv version)

# Exit on error
set -e

echo "----------------------------------------"
echo "🚀 Repository Setup Started (using uv)"
echo "----------------------------------------"

# 1. Ensure uv is installed on the system
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' not found. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 2. Sync the environment
# This creates the .venv, installs Python, and all dependencies in one go.
# It's much faster and more reliable than manual venv creation.
echo "📥 Syncing project dependencies and Python version..."
uv sync

# 3. Setup pre-commit
echo "🧹 Setting up pre-commit hooks..."

# We use 'uv run' to execute pre-commit without manually activating the venv
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🪝  Installing pre-commit hooks..."
    uv run pre-commit install
else
    echo "⚠️  No .pre-commit-config.yaml found, skipping hook installation."
fi

# 4. Run formatting
echo "✨ Running 'make fmt'..."
# 'uv run' automatically uses the .venv created by 'uv sync'
uv run make fmt

echo "----------------------------------------"
echo "✅ Setup Complete!"
echo "To run your API, you can use: uv run uvicorn app.main:app"
echo "Or activate the environment: source .venv/bin/activate"
echo "----------------------------------------"