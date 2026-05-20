from proforma_generator.contract import Contract, PaymentScheduleMilestone
from proforma_generator import price_index
from proforma_generator import billing
from typing import TypedDict
from string import capwords
from decimal import Decimal
from proforma_generator.price_index import (
    CPI_data,
    fetch_cpi_data,
    format_month_2digits,
)
from babel.numbers import format_currency, format_percent
from babel.dates import format_date
from datetime import date


class CalculatedData(TypedDict):
    contract_id: int
    title: str
    client: str
    client_project_manager: str
    client_tax_id: int
    address: dict[str, str]
    proposal: int
    proposal_date: date
    contract_amount: Decimal
    currency: str
    locale: str
    payment_schedule: list[PaymentScheduleMilestone]
    milestone_amounts: list[Decimal]
    date_today: str
    milestone_to_bill: list[int]
    base_month: date
    current_month: str
    cpi_variation: Decimal
    subtotal_amount: Decimal
    adjustment_amount: Decimal
    adjusted_subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    cpi_data: list[CPI_data]


class NormalizedData(TypedDict):
    contract_id: int
    title: str
    client: str
    client_project_manager: str
    client_tax_id: int
    address1: str
    address2: str
    proposal: int
    proposal_date: str
    contract_amount: str
    currency: str
    payment_schedule: list[PaymentScheduleMilestone]
    milestone_amounts: list[str]
    date_today: str
    base_month: str
    current_month: str
    cpi_variation: str
    subtotal_amount: str
    adjustment_amount: str
    adjusted_subtotal: str
    tax_amount: str
    total_amount: str
    cpi_data: list[CPI_data]


def generate_calculated_data(
    contract: Contract, milestones: list[int]
) -> CalculatedData:

    cpi_variation = price_index.calculate_cpi_variation(contract)

    subtotal_amount = billing.calculate_subtotal(contract, milestones)

    adjustment_amount = billing.calculate_adjustment_amount(
        contract, milestones, (cpi_variation * 100)
    )

    adjusted_subtotal = billing.calculate_adjusted_subtotal(
        subtotal_amount, adjustment_amount
    )

    tax_amount = billing.calculate_tax(adjusted_subtotal)
    locale = contract.get_locale()
    return {
        "contract_id": contract.contract_id,
        "title": contract.title,
        "client": contract.client,
        "client_project_manager": contract.client_project_manager,
        "client_tax_id": contract.client_tax_id,
        "address": contract.address,
        "proposal": contract.proposal,
        "proposal_date": contract.get_contract_date(),
        "contract_amount": Decimal(contract.contract_amount),
        "currency": contract.currency,
        "locale": locale,
        "payment_schedule": contract.payment_schedule_with_amount(),
        "milestone_amounts": contract.calculate_milestone_amount(),
        "date_today": format_date(date.today(), format="short", locale=locale),
        "milestone_to_bill": milestones,
        "base_month": contract.get_cpi_base_date(),
        "current_month": format_date(date.today(), format="MM/yyyy", locale=locale),
        "cpi_variation": cpi_variation,
        "subtotal_amount": subtotal_amount,
        "adjustment_amount": adjustment_amount,
        "adjusted_subtotal": adjusted_subtotal,
        "tax_amount": tax_amount,
        "total_amount": billing.calculate_total_amount(adjusted_subtotal, tax_amount),
        "cpi_data": fetch_cpi_data(contract),
    }


def normalize_data(calculated_data: CalculatedData) -> NormalizedData:

    address2: str = f"{capwords(calculated_data['address']["city"])}, \
           {calculated_data['address']["state"].upper()} - \
            {calculated_data['address']["country"].upper()}"

    f_milestone_amounts = [
        format_currency(
            milestone,
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        )
        # f"{money(two_decimals(milestone), calculated_data["currency"], calculated_data["locale"],)}"
        for milestone in calculated_data["milestone_amounts"]
    ]

    return {
        "contract_id": calculated_data["contract_id"],
        "title": capwords(calculated_data["title"]),
        "client": calculated_data["client"].upper(),
        "client_project_manager": capwords(calculated_data["client_project_manager"]),
        "client_tax_id": calculated_data["client_tax_id"],
        "address1": capwords(calculated_data["address"]["1stLine"]),
        "address2": address2,
        "proposal": calculated_data["proposal"],
        "proposal_date": format_date(
            calculated_data["proposal_date"],
            format="MMM/YYYY",
            locale=calculated_data["locale"],
        ),
        "contract_amount": format_currency(
            calculated_data["contract_amount"],
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        ),
        "currency": calculated_data["currency"],
        "milestone_amounts": f_milestone_amounts,
        "payment_schedule": calculated_data["payment_schedule"],
        "date_today": calculated_data["date_today"],
        "base_month": format_date(
            calculated_data["base_month"],
            format="MMM/YYYY",
            locale=calculated_data["locale"],
        ),
        "current_month": format_date(
            date.today(),
            format="MMM/YYYY",
            locale=calculated_data["locale"],
        ),
        "cpi_variation": format_percent(
            calculated_data["cpi_variation"],
            format="#,##0.00%",
            locale=calculated_data["locale"],
        ),
        "subtotal_amount": format_currency(
            calculated_data["subtotal_amount"],
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        ),
        "adjustment_amount": format_currency(
            calculated_data["adjustment_amount"],
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        ),
        "adjusted_subtotal": format_currency(
            calculated_data["adjusted_subtotal"],
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        ),
        "tax_amount": format_currency(
            calculated_data["tax_amount"],
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        ),
        "total_amount": format_currency(
            calculated_data["total_amount"],
            currency=calculated_data["currency"],
            locale=calculated_data["locale"],
        ),
        "cpi_data": format_month_2digits(calculated_data["cpi_data"]),
    }
