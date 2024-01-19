from datetime import datetime, timedelta


def calculate_expired_date(current_date: datetime) -> int:
    # Получаем текущий день месяца
    current_day = current_date.day

    # Если текущий день 29, 30 или 31, то делаем его 1
    if current_day in [29, 30, 31]:
        next_date = current_date.replace(day=1) + timedelta(days=1)
        while next_date.day != 1:
            next_date += timedelta(days=1)
    else:
        next_date = current_date

    # Увеличиваем месяц на 1
    if next_date.month == 12:
        # Если месяц декабрь, то увеличиваем год на 1 и делаем месяц январь
        next_date = next_date.replace(year=next_date.year + 1, month=1)
    else:
        next_date = next_date.replace(month=next_date.month + 1)

    return int(next_date.timestamp())
