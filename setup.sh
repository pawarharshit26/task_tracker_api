#!/bin/bash

# setup.sh - Environment setup script for pragya_api

# Exit on error
set -e

echo "----------------------------------------"
echo "🚀 Repository Setup Started"
echo "----------------------------------------"

# 1. Create virtual environment venv
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment 'venv'..."
    python3 -m venv venv
else
    echo "ℹ️  Virtual environment 'venv' already exists."
fi

# 2. Install poetry in the virtual environment
echo "🛠️  Updating pip and installing poetry in venv..."
./venv/bin/pip install --upgrade pip
./venv/bin/pip install poetry

# 3. Run poetry install
echo "📥 Installing project dependencies..."
# Activation ensures poetry uses the venv we just created/updated
source venv/bin/activate
poetry install

# 4. Setup precommit formatting and run make fmt
echo "🧹 Setting up formatting..."
# Ensure pre-commit is installed
pip install pre-commit

# If there's a pre-commit config, install the hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🪝  Installing pre-commit hooks..."
    pre-commit install
else
    echo "⚠️  No .pre-commit-config.yaml found, skipping hook installation."
fi

# Run the formatting command as requested
echo "✨ Running 'make fmt'..."
make fmt

echo "----------------------------------------"
echo "✅ Setup Complete!"
echo "To activate the environment, run:"
echo "source venv/bin/activate"
echo "----------------------------------------"
