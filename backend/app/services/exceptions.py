class AppError(Exception):
    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class DuplicateEmailError(AppError):
    status_code = 409
    error_code = "duplicate_email"


class NotFoundError(AppError):
    status_code = 404
    error_code = "not_found"
