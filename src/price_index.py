"""Functions for calculating CPI-based contract adjustments using Argly API data"""

import utils
from contract import Contract
import requests
from typing import TypedDict
from decimal import Decimal


class CPI_data(TypedDict):
    mes: int
    anio: int
    nombre_mes: str
    valor: Decimal
    f_mes: int | str | None


def build_request_url(contract: Contract) -> str:
    """Build the Argly API request URL for the contract CPI period"""
    return f"https://api.argly.com.ar/api/ipc/range?desde={contract.get_cpi_base_date()}&hasta={utils.today('%Y-%m')}"


def fetch_cpi_data(contract: Contract) -> list[CPI_data]:
    """Fetch CPI data from the Argly API for the contract date range"""
    response = requests.get(build_request_url(contract))
    cpi_data = response.json()
    return [*cpi_data["data"]]


def calculate_cpi_variation(contract: Contract) -> Decimal:
    """Calculate accumulated INDEC CPI variation using a base index of 100"""
    index = Decimal("100")
    cpi_data = fetch_cpi_data(contract)
    for item in cpi_data[1:]:
        monthly_variation = Decimal(str(item["valor"]))
        rate = monthly_variation / 100
        index *= 1 + rate
    accumulated_variation = index - 100
    return accumulated_variation


def format_month_2digits(cpi_data: list[CPI_data]):
    for item in cpi_data:
        item["f_mes"] = f"0{item['mes']}" if item["mes"] < 10 else item["mes"]
    return cpi_data
