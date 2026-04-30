import json_handling
from datetime import date
import requests

# contract = json_handling.load_data("contract_data.json")


# Getting dates


def get_cpi_base_date(contract_pointer):
    """calculates base month for adjustment calculation"""
    if contract_pointer["proposalDate"]["month"] == 1:
        base_year = contract_pointer["proposalDate"]["year"] - 1
        base_month = 12
    else:
        base_year = contract_pointer["proposalDate"]["year"]
        base_month = contract_pointer["proposalDate"]["month"] - 1
    base_date = f"{base_year}-{base_month}"
    return base_date


def get_current_date():
    """returns a string formatted for the final PDF"""
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    return today_str


def get_contract_date(contract_pointer):
    """gets contract date from given json"""
    if contract_pointer["proposalDate"]["month"] < 10:
        return f"{contract_pointer['proposalDate']['year']}-0{contract_pointer['proposalDate']['month']}"
    else:
        return f"{contract_pointer['proposalDate']['year']}-{contract_pointer['proposalDate']['month']}"


# Formatting


def format_num_2dec(number):
    return f"{number:,.2f}"


# Handling Argly API


def define_request(base_date_function, current_date_function):
    return f"https://api.argly.com.ar/api/ipc/range?desde={base_date_function}&hasta={current_date_function}"


# response = requests.get(
#     define_request(get_cpi_base_date(contract), get_current_date()[:7])
# )
# cpi_data = response.json()


# Getting CPI data


def get_cpi_variation(cpi_data):
    """calculates INDEC CPI variation from Argly API data, assuming base index = 100"""
    index = 100
    for item in cpi_data["data"][1:]:
        rate = item["valor"] / 100
        index *= 1 + rate
    variation = index - 100
    return variation


# Calculating amounts


def calculate_milestone_amount(file_pointer):
    """
    calculates the amount of all contract's milestones
    """
    contract_amount = file_pointer["contractAmount"]

    for milestone in file_pointer["paymentSchedule"]:
        if not milestone["amount"]:
            percentage = milestone["percentage"]
            multiplier = percentage * 0.01
            amount = contract_amount * multiplier
            milestone["amount"] = format_num_2dec(amount)
    return file_pointer


# def calculate_adjusted_amount(contract_pointer, cpi_variation_function):
#     return
