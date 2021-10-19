import logging
import sys

from jsonlog.config import dev_settings
from jsonlog.formatter import LogContext, SanitizedJSONFormatter

logger = logging.getLogger(__name__)


def configure_logging(context=None, level=logging.INFO):

    root = logging.getLogger()
    root.setLevel(level)

    formatter = SanitizedJSONFormatter()

    if context:
        # When running under lambda, AWS configures a root logger with a handler;
        # we override this in the request to set a formatter that includes the context info
        aws_log_context = LogContext(context.aws_request_id, context.function_name, context.function_version)
        formatter = SanitizedJSONFormatter(aws_log_context)
        for handler in root.handlers:
            handler.setFormatter(formatter)

        # supress noisy info logs
        adjusted_level = logging.DEBUG if root.isEnabledFor(logging.DEBUG) else logging.WARNING
        logging.getLogger("mangum").setLevel(adjusted_level)
        logging.getLogger("asyncio").setLevel(adjusted_level)
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
        logger.debug("Logging configured")
