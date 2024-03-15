class QuotaExceededError(Exception):
    """Error indicating that users monthly request quota has been passed."""

    pass


class APIError(Exception):
    """Error indicating that an API error has occurred (meaning something not expected happened, like a 50x-error)."""

    pass


class ProcessingError(Exception):
    """Error indicating that an API processing error has occurred (like input data is invalid)"""

    pass


class ConnectionError(Exception):
    """Error indicating that some sort of an internet connection error has occurred."""

    pass
