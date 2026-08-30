"""
Unit tests for GCP Structured JSON Log Formatter.
"""
import json
import logging
from io import StringIO
from app.core.logging import GCPJsonFormatter


def test_gcp_json_formatter():
    """Verify log record formatting into GCP JSON structure."""
    log_output = StringIO()
    handler = logging.StreamHandler(log_output)
    formatter = GCPJsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)

    test_logger = logging.getLogger("test_logger")
    test_logger.addHandler(handler)
    test_logger.setLevel(logging.INFO)

    test_logger.info("Test log payload")

    handler.flush()
    raw_output = log_output.getvalue().strip()
    assert raw_output, "Log output should not be empty"

    log_data = json.loads(raw_output)
    assert log_data["message"] == "Test log payload"
    assert log_data["severity"] == "INFO"
    assert log_data["logger_name"] == "test_logger"
