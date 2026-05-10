from datetime import date, datetime
from rich import print
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract

from decimal import Decimal, ROUND_HALF_UP

DECIMALS = Decimal("0.01")


def two_decimals(value: Decimal) -> Decimal:
    return Decimal(value).quantize(DECIMALS, rounding=ROUND_HALF_UP)


def money(value: Decimal, currency: str) -> str:
    return f"{currency} {value:,f}"


def percentage(value: Decimal) -> str:
    return f"{value}%"


def format_date_m_y(original_date: str) -> str:
    old_format = datetime.strptime(original_date, "%Y-%m")
    return old_format.strftime("%b/%Y")


def today(date_format: str) -> str:
    today = date.today()
    return today.strftime(date_format)


def pretty_msg(msg: str, style: str, new_end: str = "\n") -> None:
    print(f"[{style}]{msg}[/{style}]", end=new_end)


# Argument validation


def validate_milestones(milestones: list[int], contract: Contract) -> None:
    from typer import Exit

    milestones_indexes = milestones_to_indexes(milestones)
    contract_milestones = len(contract.payment_schedule)
    for milestone in milestones_indexes:
        if milestone not in range(contract_milestones):
            pretty_msg("Milestone(s) out of range.", "red3")
            print(f"Selected contract has {contract_milestones} milestones. \n")
            raise Exit()


def milestones_to_indexes(milestones: list[int]) -> list[int]:
    return [milestone - 1 for milestone in milestones]
