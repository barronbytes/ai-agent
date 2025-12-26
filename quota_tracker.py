import json
from datetime import datetime, timedelta


# File to persist daily request logs
LOG_FILE = "quota_log.json"

# Logs to track request and token limits
_minute_request_log = []
_minute_input_token_log = []
_daily_request_log = []


# ------------------------------
# JSON loading
# ------------------------------

try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        _daily_request_log = [datetime.fromisoformat(ts) for ts in data.get("daily", [])]
except FileNotFoundError:
    _daily_request_log = []
except Exception:
    _daily_request_log = []


def _save_daily_log():
    """Save the daily requests for persistence."""
    data = {"daily": [dt.isoformat() for dt in _daily_request_log]}
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

# ------------------------------
# Logging function
# ------------------------------


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

    # --- Minute-based metrics ---
    _minute_request_log.append(date_time)
    _minute_input_token_log.append((date_time, input_tokens))

    # Remove entries older than one minute (for RPM and TPM)
    one_minute_ago = date_time - timedelta(minutes=1)
    _minute_request_log[:] = [dt for dt in _minute_request_log if dt > one_minute_ago]
    _minute_input_token_log[:] = [(dt, tokens) for dt, tokens in _minute_input_token_log if dt > one_minute_ago]

    # --- Daily metrics ---
    _daily_request_log.append(date_time)

    # Remove entries older than one day (for RPD)
    today = date_time.date()
    _daily_request_log[:] = [dt for dt in _daily_request_log if dt.date() == today]

    # --- Save to daily log ---
    _save_daily_log


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
    """Return threshold limit for requests per day (RPD)."""
    return 20


def threshold_rpm() -> int:
    """Return threshold limit for requests per minute (RPM)."""
    return 5


def threshold_tpm() -> int:
    """Return threshold limit for input tokens per minute (TPM)."""
    return 250000
