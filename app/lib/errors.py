class DataAccessError(Exception):
    """Raised when database operations fail."""

    def __init__(self, message: str, *, original: Exception | None = None):
        super().__init__(message)
        self.original = original
