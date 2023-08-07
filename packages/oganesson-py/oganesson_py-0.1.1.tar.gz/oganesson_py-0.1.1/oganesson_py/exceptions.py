from click import ClickException


class QualityFailureException(ClickException):
    """Raised when quality metrics failed"""
