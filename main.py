#!/usr/bin/env python3
import re
from datetime import datetime

MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

DATE_DOT_RE = re.compile(r"^(\d{1,2})\.(\d{1,2})\.(\d{4})$")
DATE_TEXT_RE = re.compile(r"^(\d{1,2})\s+([а-яё]+)\s+(\d{4})$", re.IGNORECASE)


def parse_date(value: str) -> datetime:
    value = value.strip()
    dot_match = DATE_DOT_RE.match(value)
    if dot_match:
        day, month, year = map(int, dot_match.groups())
        return datetime(year, month, day)

    text_match = DATE_TEXT_RE.match(value)
    if text_match:
        day_str, month_name, year_str = text_match.groups()
        day = int(day_str)
        year = int(year_str)
        month_key = month_name.lower()
        if month_key not in MONTHS:
            raise ValueError(f"Неизвестный месяц: {month_name}")
        return datetime(year, MONTHS[month_key], day)

    raise ValueError(
        "Неверный формат. Примеры: 12.02.2021 или 12 февраля 2021"
    )


def read_date(prompt: str) -> datetime:
    while True:
        raw = input(prompt)
        try:
            return parse_date(raw)
        except ValueError as exc:
            print(f"Ошибка: {exc}")


def format_delta(delta_seconds: int) -> str:
    hours = abs(delta_seconds) // 3600
    days = hours // 24
    label = "осталось" if delta_seconds > 0 else "прошло"
    if delta_seconds == 0:
        return "Даты совпадают. Прошло 0 дней и 0 часов."
    return f"{label.capitalize()} {days} дней и {hours} часов."


def main() -> None:
    print("Калькулятор дат")
    first_date = read_date("Введите первую дату: ")
    second_date = read_date("Введите вторую дату: ")

    delta = second_date - first_date
    delta_seconds = int(delta.total_seconds())

    print(format_delta(delta_seconds))


if __name__ == "__main__":
    main()
