"""
Utility functions and modules for the Dama UI application.

This package contains various utility functions and modules that are used
throughout the Dama UI application, including logging configuration,
request processing, token counting, and usage tracking.
"""

from .logging_config import setup_logging
from .request_processor import process_request
from .token_counter import count_tokens
from .usage_tracking import update_usage, get_usage

__all__ = [
    'setup_logging',
    'process_request',
    'count_tokens',
    'update_usage',
    'get_usage',
]

# Initialize logging when the utils package is imported
setup_logging()

# You can add any package-level initialization code here if needed.
# For example:
#
# def initialize_utils():
#     """Initialize any utility-related resources or settings."""
#     pass
#
# initialize_utils()

# If you have any shared constants or utility functions that don't fit
# into any specific module, you can define them here:
#
# MAX_RETRIES = 3
#
# def retry_operation(operation, max_retries=MAX_RETRIES):
#     """Retry an operation with exponential backoff."""
#     # Implementation here
#     pass