import json_handling
from datetime import date
import requests
import utils

# Getting contract and CPI dates


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


def get_contract_date(contract_pointer):
    """gets contract date from given json"""
    if contract_pointer["proposalDate"]["month"] < 10:
        return f"{contract_pointer['proposalDate']['year']}-0{contract_pointer['proposalDate']['month']}"
    else:
        return f"{contract_pointer['proposalDate']['year']}-{contract_pointer['proposalDate']['month']}"


# Handling Argly API


def define_request(contract_pointer):
    return f"https://api.argly.com.ar/api/ipc/range?desde={get_cpi_base_date(contract_pointer)}&hasta={utils.get_current_date("%Y-%m")}"


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
            milestone["amount"] = utils.format_num_2dec(amount)
    return file_pointer


def calculate_adjustment_amount(contract_pointer, milestone, cpi_data):
    float_og_amount = utils.format_string_to_float(
        contract_pointer["paymentSchedule"][milestone]["amount"]
    )
    variation = get_cpi_variation(cpi_data) / 100
    adjustment_amount = float_og_amount * variation
    return adjustment_amount


def calculate_adjusted_subtotal(contract_pointer, milestone, cpi_data):
    og_amount = utils.format_string_to_float(
        contract_pointer["paymentSchedule"][milestone]["amount"]
    )

    adjustment = calculate_adjustment_amount(contract_pointer, milestone, cpi_data)
    return adjustment + og_amount
