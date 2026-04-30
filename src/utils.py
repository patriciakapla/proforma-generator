from datetime import date

# Formatting


def format_num_2dec(number):
    return f"{number:,.2f}"


def format_string_to_float(value):
    new_value = value.replace(",", "")
    return float(new_value)


def get_current_date():
    """returns a string formatted for the final PDF"""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    return today_str
