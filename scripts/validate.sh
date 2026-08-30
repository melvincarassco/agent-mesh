#!/usr/bin/env bash
# Architecture & Standards Validation Script for agent-mesh
set -euo pipefail

echo "========================================="
echo "  Carassco Labs - Architecture Validator"
echo "========================================="

echo "🔍 Checking required directory structure..."

REQUIRED_DIRS=(
    "app"
    "tests"
    "docs"
    "scripts"
    "infrastructure"
    ".github"
    "docker"
    "config"
    "architecture"
    "examples"
    "assets"
    "docs/adr"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  [OK] Directory exists: $dir"
    else
        echo "  [FAIL] Missing required directory: $dir"
        exit 1
    fi
done

echo ""
echo "🔍 Checking mandatory Architecture Decision Records (ADRs)..."
REQUIRED_ADRS=(
    "docs/adr/ADR-001-why-google-cloud-platform.md"
    "docs/adr/ADR-002-why-fastapi.md"
    "docs/adr/ADR-003-why-docker.md"
    "docs/adr/ADR-004-why-cloud-run.md"
    "docs/adr/ADR-005-why-github-actions.md"
)

for adr in "${REQUIRED_ADRS[@]}"; do
    if [ -f "$adr" ]; then
        echo "  [OK] ADR exists: $adr"
    else
        echo "  [FAIL] Missing ADR: $adr"
        exit 1
    fi
done

echo ""
echo "🎉 All agent-mesh architectural checks PASSED!"
