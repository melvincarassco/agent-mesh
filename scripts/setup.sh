#!/usr/bin/env bash
# Local environment setup script for agent-mesh
set -euo pipefail

echo "========================================="
echo "  Carassco Labs - Local Setup Script"
echo "========================================="

if [ ! -f .env ]; then
    echo "📄 Creating .env from .env.example..."
    cp .env.example .env
fi

echo "✅ Environment setup complete."
