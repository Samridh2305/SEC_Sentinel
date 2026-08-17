
class AppException(Exception):
    status_code = 500
    detail = "Application error"

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail


class ReportExtractionException(AppException):
    status_code = 422
    detail = "Could not extract readable text from file."


class DatabaseSaveException(AppException):
    status_code = 500
    detail = "Could not save report to database."


class ReportNotFoundException(AppException):
    status_code = 404
    detail = "Report not found."


class InvalidReportIdException(AppException):
    status_code = 400
    detail = "Invalid report ID."