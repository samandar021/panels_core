from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    """Базовая модель."""
    __name__: str
