from contract import Contract, PaymentScheduleMilestone
from utils import today, format_date_m_y, two_decimals, money, percentage
import price_index
import billing
from typing import TypedDict
from string import capwords
from decimal import Decimal
from price_index import CPI_data, fetch_cpi_data


class CalculatedData(TypedDict):
    contract_id: int
    title: str
    client: str
    client_project_manager: str
    client_tax_id: int
    address: dict[str, str]
    proposal: int
    proposal_date: str
    contract_amount: Decimal
    currency: str
    payment_schedule: list[PaymentScheduleMilestone]
    milestone_amounts: list[Decimal]
    date_today: str
    milestone_to_bill: list[int]
    base_month: str
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
        contract, milestones, cpi_variation
    )

    adjusted_subtotal = billing.calculate_adjusted_subtotal(
        subtotal_amount, adjustment_amount
    )

    tax_amount = billing.calculate_tax(adjusted_subtotal)

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
        "payment_schedule": contract.payment_schedule_with_amount(),
        "milestone_amounts": contract.calculate_milestone_amount(),
        "date_today": today("%m/%d/%Y"),
        "milestone_to_bill": milestones,
        "base_month": contract.get_cpi_base_date(),
        "current_month": today("%m/%Y"),
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
            {capwords(calculated_data['address']["country"])}"

    f_milestone_amounts = [
        f"{money(two_decimals(milestone), "$")}"
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
        "proposal_date": format_date_m_y(calculated_data["proposal_date"]),
        "contract_amount": f"$ {two_decimals(calculated_data["contract_amount"])}",
        "currency": calculated_data["currency"].upper(),
        "milestone_amounts": f_milestone_amounts,
        "payment_schedule": calculated_data["payment_schedule"],
        "date_today": calculated_data["date_today"],
        "base_month": format_date_m_y(calculated_data["base_month"]),
        "current_month": today("%b/%Y"),
        "cpi_variation": percentage(two_decimals(calculated_data["cpi_variation"])),
        "subtotal_amount": money(two_decimals(calculated_data["subtotal_amount"]), "$"),
        "adjustment_amount": money(
            two_decimals(calculated_data["adjustment_amount"]), "$"
        ),
        "adjusted_subtotal": money(
            two_decimals(calculated_data["adjusted_subtotal"]), "$"
        ),
        "tax_amount": money(two_decimals(calculated_data["tax_amount"]), "$"),
        "total_amount": money(two_decimals(calculated_data["total_amount"]), "$"),
        "cpi_data": calculated_data["cpi_data"],
    }
