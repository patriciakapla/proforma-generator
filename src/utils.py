from datetime import date, datetime
from rich import print
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contract import Contract

# Formatting


def format_num_2dec(number: int | float) -> str:
    return f"{number:,.2f}"


def format_string_to_float(value: str) -> float:
    new_value = value.replace(",", "")
    return float(new_value)


def format_date_m_y(original_date: str) -> str:
    old_format = datetime.strptime(original_date, "%Y-%m")
    return old_format.strftime("%b/%Y")


def today(date_format: str) -> str:
    today = date.today()
    return today.strftime(date_format)


# Validate milestone


def validate_milestones(milestones: list[int], contract: Contract) -> None:
    from typer import Exit

    contract_milestones = len(contract.payment_schedule)
    for milestone in milestones:
        if milestone not in range(contract_milestones):
            print(
                f"Milestone out of range. Selected contract has {contract_milestones} milestones."
            )
            raise Exit()


def milestones_to_indexes(milestones: list[int]) -> list[int]:
    return [milestone - 1 for milestone in milestones]
