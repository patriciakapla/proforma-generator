from dataclasses import dataclass
from rich import print
from typing import TypedDict
from decimal import Decimal
from utils import milestones_to_indexes


class PaymentScheduleMilestone(TypedDict):
    description: str
    percentage: int
    billed: bool | None
    amount: Decimal


@dataclass
class Contract:
    contract_id: int
    title: str
    client: str
    client_tax_id: int
    client_project_manager: str
    address: dict[str, str]
    proposal: int
    proposal_date: dict[str, int]
    contract_amount: int
    currency: str
    payment_schedule: list[PaymentScheduleMilestone]

    def print_contract(self, milestones: list[int]) -> None:
        milestones_indexes = milestones_to_indexes(milestones)
        print(f"Selected contract: [yellow]{self.title}[/yellow]")
        for milestone in milestones_indexes:
            if milestone:  # if called from generate_proforma command
                print(
                    f"Selected milestone: [yellow]{self.payment_schedule[milestone]["percentage"]}% - {self.payment_schedule[milestone]["description"]}[/yellow]"
                )

    def print_milestones(self) -> None:
        for i, _ in enumerate(self.payment_schedule):
            print(f"[bold yellow][{i+1}]: [/bold yellow]", sep="", end=" ")
            print(
                f"[default]{self.payment_schedule[i]["percentage"]}% - [/default]",
                sep="",
                end=" ",
            )
            print(self.payment_schedule[i]["description"])
            if self.payment_schedule[i]["billed"]:
                print("[green]Billed[/green]")
            else:
                print("[red]Not billed[/red]")
            print()

    def calculate_milestone_amount(
        self,
    ) -> list[Decimal]:
        milestone_amounts: list[Decimal] = []
        for milestone in self.payment_schedule:
            multiplier = Decimal(str(milestone["percentage"])) * Decimal("0.01")
            amount = self.contract_amount * multiplier
            milestone_amounts.append(amount)
        return milestone_amounts

    def get_contract_date(self) -> str:
        """gets contract date from json"""
        return f"{self.proposal_date["year"]}-{self.proposal_date["month"]}"

    def get_cpi_base_date(self) -> str:
        """calculates base month for adjustment calculation"""
        if self.proposal_date["month"] == 1:
            base_year = self.proposal_date["year"] - 1
            base_month = 12
        else:
            base_year = self.proposal_date["year"]
            base_month = self.proposal_date["month"] - 1
        return f"{base_year}-{base_month}"

    def payment_schedule_with_amount(self) -> list[PaymentScheduleMilestone]:
        updated_payment_schedule: list[PaymentScheduleMilestone] = []
        for i, milestone in enumerate(self.payment_schedule):
            updated_payment_schedule.append(
                {
                    "description": milestone["description"],
                    "percentage": milestone["percentage"],
                    "billed": milestone["billed"],
                    "amount": self.calculate_milestone_amount()[i],
                }
            )
        return updated_payment_schedule
