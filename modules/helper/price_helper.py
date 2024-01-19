from decimal import Decimal


class PriceHelper:
    @staticmethod
    def prepare_amount(amount: Decimal) -> Decimal:  # Используем Decimal для точных вычислений
        """Функция которая в текущей реализации просто возвращает переданное значение"""
        return amount
