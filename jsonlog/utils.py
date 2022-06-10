import logging
import sys
from typing import List

from jsonlog.config import dev_settings
from jsonlog.formatter import LogContext, SanitizedJSONFormatter

logger = logging.getLogger(__name__)


def configure_logging(context=None, level=logging.INFO, suppressed_loggers: List[str] = None):

    root = logging.getLogger()
    root.setLevel(level)

    formatter = SanitizedJSONFormatter()

    adjusted_level = logging.ERROR
    if root.isEnabledFor(logging.DEBUG):
        adjusted_level = logging.WARNING

    if suppressed_loggers:
        for log in suppressed_loggers:
            logging.getLogger(log).setLevel(adjusted_level)

    if context:
        # When running under lambda, AWS configures a root logger with a handler;
        # we override this in the request to set a formatter that includes the context info
        aws_log_context = LogContext(context.aws_request_id, context.function_name, context.function_version)
        formatter = SanitizedJSONFormatter(aws_log_context)
        for handler in root.handlers:
            handler.setFormatter(formatter)

        # supress noisy info logs
        logging.getLogger("mangum").setLevel(adjusted_level)
        logging.getLogger("asyncio").setLevel(adjusted_level)
        logging.getLogger("boto").setLevel(adjusted_level)
        logging.getLogger("botocore").setLevel(adjusted_level)

        logger.debug("Logging configured")

    elif dev_settings.is_under_test:
        # When not running under pytest, again the root logger is already configured;
        # override pytests handler to set a request-specific formatter that includes the test
        # data in the context
        pytest_log_context = LogContext("pytest", "", "")
        formatter = SanitizedJSONFormatter(pytest_log_context)
        for handler in root.handlers:
            handler.setFormatter(formatter)
        logger.debug("Logging configured")

    else:
        # When not running under lambda or pytest, just create our own handler & formatter
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        root.addHandler(handler)
        logging.getLogger("boto").setLevel(adjusted_level)
        logging.getLogger("botocore").setLevel(adjusted_level)

        logger.debug("Logging configured")
