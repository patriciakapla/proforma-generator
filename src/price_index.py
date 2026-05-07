"""Functions for calculating CPI-based contract adjustments using Argly API data"""

import utils
from contract import Contract
import requests
from typing import TypedDict


class CPI_data(TypedDict):
    mes: int
    anio: int
    nombre_mes: str
    valor: float


def build_request_url(contract: Contract) -> str:
    """Build the Argly API request URL for the contract CPI period"""
    return f"https://api.argly.com.ar/api/ipc/range?desde={contract.get_cpi_base_date()}&hasta={utils.today('%Y-%m')}"


def fetch_cpi_data(contract: Contract) -> list[CPI_data]:
    """Fetch CPI data from the Argly API for the contract date range"""
    response = requests.get(build_request_url(contract))
    cpi_data = response.json()
    return [*cpi_data["data"]]


def calculate_cpi_variation(contract: Contract) -> float:
    """Calculate accumulated INDEC CPI variation using a base index of 100"""
    index = 100
    cpi_data = fetch_cpi_data(contract)
    for item in cpi_data[1:]:
        monthly_variation = item["valor"]
        rate = monthly_variation / 100
        index *= 1 + rate
    accumulated_variation = index - 100
    return accumulated_variation
