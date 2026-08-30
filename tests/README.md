# Automated Test Suite (`tests/`)

Comprehensive test suite structure for unit, integration, and end-to-end testing in accordance with [Carassco Labs Testing Standards](file:///Users/dalehendriques/Downloads/MELVIN_WORK/carassco-labs/handbook/docs/12-testing-standards.md).

## Test Suite Hierarchy

```text
tests/
├── unit/         # Fast isolated component tests (no external I/O)
├── integration/  # Multi-component tests with mocked/test database & GCP APIs
├── e2e/          # End-to-End API endpoint validation tests (HTTPX / TestClient)
├── fixtures/     # Reusable pytest fixtures & sample data payloads
└── conftest.py   # Global pytest configuration & async loop setup
```

## Running Tests

```bash
# Run all unit tests
pytest tests/unit

# Run full test suite with coverage
pytest --cov=app --cov-report=term-missing tests/
```
