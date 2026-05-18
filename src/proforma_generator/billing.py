from proforma_generator.contract import Contract
from proforma_generator import utils
from decimal import Decimal


def calculate_subtotal(contract: Contract, milestones: list[int]) -> Decimal:
    subtotal = Decimal("0")
    milestones_index = utils.milestones_to_indexes(milestones)
    for milestone in milestones_index:
        amount: list[Decimal] = contract.calculate_milestone_amount()
        subtotal += amount[milestone]
    return subtotal


def calculate_adjustment_amount(
    contract: Contract, milestones: list[int], cpi_variation: Decimal
) -> Decimal:
    """Calculate the CPI adjustment amount for contract milestones"""

    variation = cpi_variation / Decimal("100")
    milestones_index = utils.milestones_to_indexes(milestones)
    original_amount: list[Decimal] = contract.calculate_milestone_amount()

    return sum(
        (original_amount[milestone] * variation for milestone in milestones_index),
        Decimal("0"),
    )


def calculate_adjusted_subtotal(
    subtotal_amount: Decimal,
    adjusted_amount: Decimal,
) -> Decimal:
    """Calculate the milestone amount after CPI adjustment"""
    return adjusted_amount + subtotal_amount


def calculate_tax(adjusted_subtotal: Decimal) -> Decimal:
    return adjusted_subtotal * Decimal("0.21")


def calculate_total_amount(adjusted_subtotal: Decimal, tax: Decimal) -> Decimal:
    return adjusted_subtotal + tax
