from datetime import date
import utils
from pathlib import Path
from contract import Contract
import requests
import json_handling

# Getting Argly API price index data


def define_request(contract: Contract) -> str:
    return f"https://api.argly.com.ar/api/ipc/range?desde={contract.get_cpi_base_date()}&hasta={utils.today('%Y-%m')}"


def loading_api_data(contract: Contract) -> list[dict[str, int | str | float]]:
    response = requests.get(define_request(contract))
    cpi_data = response.json()
    return [*cpi_data["data"]]


def get_cpi_variation(contract: Contract) -> float:
    """calculates INDEC CPI variation from Argly API data, assuming base index = 100"""
    index = 100
    cpi_data = loading_api_data(contract)
    for item in cpi_data[1:]:
        value = float(item["valor"])
        rate = value / 100
        index *= 1 + rate
    variation = index - 100
    return variation


# Calculating amounts


def calculate_adjustment_amount(contract: Contract, milestone: int) -> float:

    float_og_amount = utils.format_string_to_float(
        contract.payment_schedule[milestone]["amount"]
    )
    variation = get_cpi_variation(contract) / 100
    adjustment_amount = float_og_amount * variation
    return adjustment_amount


def calculate_adjusted_subtotal(contract: Contract, milestone: int) -> float:
    og_amount = utils.format_string_to_float(
        contract.payment_schedule[milestone]["amount"]
    )
    adjustment = calculate_adjustment_amount(contract, milestone)
    return adjustment + og_amount
