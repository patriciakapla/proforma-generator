from contract import Contract, PaymentScheduleMilestone
import utils
import price_index
import billing
from typing import TypedDict


class CalculatedData(TypedDict):
    contract_id: int
    title: str
    client: str
    client_project_manager: str
    client_tax_id: int
    proposal: int
    proposal_date: str
    contract_amount: int
    currency: str
    payment_schedule: list[PaymentScheduleMilestone]
    milestone_amounts: list[float]
    date_today: str
    address: dict[str, str]
    milestone_to_bill: list[int]
    base_month: str
    current_month: str
    cpi_variation: float
    subtotal_amount: float
    adjustment_amount: float
    adjusted_subtotal: float


def generate_calculated_data(
    contract: Contract, milestones: list[int]
) -> CalculatedData:
    cpi_variation = price_index.calculate_cpi_variation(contract)
    subtotal_amount = billing.calculate_subtotal(contract, milestones)
    adjustment_amount = billing.calculate_adjustment_amount(
        contract, milestones, cpi_variation
    )

    return {
        "contract_id": contract.contract_id,
        "title": contract.title,
        "client": contract.client,
        "client_project_manager": contract.client_project_manager,
        "client_tax_id": contract.client_tax_id,
        "address": contract.address,
        "proposal": contract.proposal,
        "proposal_date": contract.get_contract_date(),
        "contract_amount": contract.contract_amount,
        "currency": contract.currency,
        "payment_schedule": contract.payment_schedule_with_amount(),
        "date_today": utils.today("%Y-%m-%d"),
        "milestone_to_bill": milestones,
        "milestone_amounts": contract.calculate_milestone_amount(),
        "base_month": contract.get_cpi_base_date(),
        "current_month": utils.today("%Y-%m"),
        "cpi_variation": cpi_variation,
        "subtotal_amount": subtotal_amount,
        "adjustment_amount": adjustment_amount,
        "adjusted_subtotal": billing.calculate_adjusted_subtotal(
            subtotal_amount, adjustment_amount
        ),
    }


# testing
def printdata(data: CalculatedData):
    print(*data, sep="\n")


def printdatatype(data: CalculatedData):
    for k, v in data.items():
        print(f"{k}: {v}\n")
