from contract import Contract
import utils


def calculate_subtotal(contract: Contract, milestones: list[int]) -> float:
    subtotal = 0
    milestones_index = utils.milestones_to_indexes(milestones)
    for milestone in milestones_index:
        amount: list[float] = contract.calculate_milestone_amount()
        subtotal += amount[milestone]
    return subtotal


def calculate_adjustment_amount(
    contract: Contract, milestones: list[int], cpi_variation: float
) -> float:
    """Calculate the CPI adjustment amount for a contract milestone"""
    adjustment_list: list[float] = []
    for milestone in milestones:
        original_amount: list[float] = contract.calculate_milestone_amount()
        variation = cpi_variation / 100
        adjustment_amount = original_amount[milestone] * variation
        adjustment_list.append(adjustment_amount)
    adjustment_amount = sum(adjustment_list)
    return adjustment_amount


def calculate_adjusted_subtotal(
    subtotal_amount: float,
    adjusted_amount: float,
) -> float:
    """Calculate the milestone amount after CPI adjustment"""
    return adjusted_amount + subtotal_amount
