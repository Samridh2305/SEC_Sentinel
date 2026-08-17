
class AppException(Exception):
    status_code = 500
    detail = "Application error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class DatabaseException(AppException):
    status_code = 503
    detail = "The database is temporarily unavailable."


class BadRequestException(AppException):
    status_code = 400
    detail = "The request is invalid."


class NotFoundException(AppException):
    status_code = 404
    detail = "The requested resource was not found."


class ServiceException(AppException):
    status_code = 502
    detail = "An external service is temporarily unavailable."


class ProcessingException(AppException):
    status_code = 422
    detail = "The request could not be processed."
