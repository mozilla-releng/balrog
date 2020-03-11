class BadDataError(Exception):
    """Raised when a client sends data that appears to be invalid."""

    pass


class BlobValidationError(ValueError):
    def __init__(self, message, errors, *args, **kwargs):
        self.errors = errors
        super(BlobValidationError, self).__init__(message, *args, **kwargs)


class SignoffRequiredError(Exception):
    """Raised when someone attempts to directly modify an object that requires
    signoff."""


class PermissionDeniedError(Exception):
    pass


class ReadOnlyError(Exception):
    """Raised when a release marked as read-only is attempted to be changed."""
