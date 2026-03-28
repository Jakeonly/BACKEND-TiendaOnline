"""
Excepciones personalizadas para la Tienda Online.
Sigue el estándar de manejo de errores de la capa core.
"""

from fastapi import status


class AppException(Exception):
    """Base para todas las excepciones de la Tienda Online."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        code: str | None = None,
        details: dict | list | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.code = code or "INTERNAL_SERVER_ERROR"
        self.details = details
        super().__init__(message)


class NotFoundError(AppException):
    """Se lanza cuando un producto, usuario o categoría no existe."""

    def __init__(self, message: str = "Recurso no encontrado", details: dict | list | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            details=details,
        )


class BadRequestError(AppException):
    """Para errores de lógica de negocio o peticiones mal formadas."""

    def __init__(self, message: str, details: dict | list | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            details=details,
        )


class ConflictError(AppException):
    """Para cuando se intenta duplicar algo (ejemplo: mismo email de usuario)."""

    def __init__(self, message: str, details: dict | list | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            code="CONFLICT",
            details=details,
        )


class InsufficientStockError(AppException):
    """Excepción específica para la tienda cuando no hay suficiente producto."""

    def __init__(self, message: str = "Stock insuficiente para realizar la compra"):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INSUFFICIENT_STOCK",
        )