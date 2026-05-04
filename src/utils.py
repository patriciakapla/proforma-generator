from datetime import date
from rich import print

# Formatting


def format_num_2dec(number: int | float) -> str:
    return f"{number:,.2f}"


def format_string_to_float(value: str) -> float:
    new_value = value.replace(",", "")
    return float(new_value)


def today(date_format: str) -> str:
    today = date.today()
    today_str = today.strftime(date_format)
    return today_str
