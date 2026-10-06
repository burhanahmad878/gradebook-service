"""Custom exception hierarchy for the gradebook service."""


class GradebookError(Exception):
    """Base class for all gradebook service errors."""


class ValidationError(GradebookError):
    """Raised when request payload or data validation fails."""


class NotFoundError(GradebookError):
    """Raised when a requested resource is not found."""


class ConflictError(GradebookError):
    """Raised when a resource already exists or conflicts with existing state."""