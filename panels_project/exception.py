from fastapi import HTTPException


class Is2FAException(HTTPException):
    """Если пользователю нужно пройти 2fa авторизацию"""


class AuthorizationException(HTTPException):
    """Если пользователь не авторизован"""


class NotFoundPanelByDomainException(HTTPException):
    """Если панель не найдена по домену"""
