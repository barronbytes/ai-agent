from datetime import datetime, timedelta


# Logs to track request and token limits
_minute_request_log = []
_minute_input_token_log = []
_daily_request_log = []


def log_request(input_tokens: int) -> None:
    '''
    Tracks API usage metrics for Google Gemini model calls to help manage
    requests per minute (RPM), input tokens per minute (TPM), and requests per day (RPD).

    This is useful for monitoring usage, enforcing limits, and verbose logging of
    API consumption during AI agent sessions.

    Args:
        input_tokens: The input tokens from a successful request to AI model.
    Returns:
        Not applicable.
    '''
    date_time = datetime.now()

    # Log for minute-based metrics
    _minute_request_log.append(date_time)
    _minute_input_token_log.append((date_time, input_tokens))

    # Log for daily metrics
    _daily_request_log.append(date_time)

    # Remove entries older than one minute (for RPM and TPM)
    one_minute_ago = date_time - timedelta(minutes=1)
    _minute_request_log[:] = [dt for dt in _minute_request_log if dt > one_minute_ago]
    _minute_input_token_log[:] = [(dt, tokens) for dt, tokens in _minute_input_token_log if dt > one_minute_ago]

    # Remove entries older than one day (for RPD)
    today = date_time.date()
    _daily_request_log[:] = [dt for dt in _daily_request_log if dt.date() == today]


def get_rpd() -> int:
    """Return number of requests in the same day."""
    return len(_daily_request_log)


def get_rpm() -> int:
    """Return number of requests in the last 60 seconds."""
    return len(_minute_request_log)


def get_tpm() -> int:
    """Return number of input tokens in the last 60 seconds."""
    return sum(tokens for dt, tokens in _minute_input_token_log)


def threshold_rpd() -> int:
    """Return threshold limit for RPD"""
    return 20


def threshold_rpm() -> int:
    """Return threshold limit for RPM"""
    return 5


def threshold_tpm() -> int:
    """Return threshold limit for TPM"""
    return 250000
