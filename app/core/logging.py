"""
GCP Structured JSON Logging Module.
Formats log records into GCP Stackdriver JSON specification.
"""
import logging
import sys
from typing import Any, Dict
from pythonjsonlogger import jsonlogger


class GCPJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter compliant with GCP Cloud Logging."""

    SEVERITY_MAP: Dict[str, str] = {
        "DEBUG": "DEBUG",
        "INFO": "INFO",
        "WARNING": "WARNING",
        "ERROR": "ERROR",
        "CRITICAL": "CRITICAL",
    }

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any]
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        
        # Standardize GCP fields
        log_record["severity"] = self.SEVERITY_MAP.get(record.levelname, "INFO")
        log_record["logger_name"] = record.name
        
        if "asctime" in log_record:
            log_record["timestamp"] = log_record.pop("asctime")
            
        # Clean up default level field if present
        if "levelname" in log_record:
            log_record.pop("levelname")


def setup_logging(log_level: str = "INFO") -> None:
    """Configures application-wide structured JSON logging to stdout."""
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.upper())
    
    # Clear existing handlers to prevent duplicate output
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = GCPJsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
