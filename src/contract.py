from dataclasses import dataclass
import utils
from rich import print
from typing import TypedDict


class PaymentScheduleMilestone(TypedDict):
    description: str
    percentage: int
    billed: bool | None
    amount: str


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
    amount: int
    currency: str
    payment_schedule: list[PaymentScheduleMilestone]

    def print_contract(self, milestones: list[int]) -> None:
        print(f"Selected contract: [yellow]{self.title}[/yellow]")
        for milestone in milestones:
            if milestone:
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
            if self.payment_schedule[i]["amount"]:
                print(self.payment_schedule[i]["amount"])
            if self.payment_schedule[i]["billed"]:
                print("[green]Billed[/green]")
            else:
                print("[red]Not billed[/red]")
            print()

    def calculate_milestone_amount(
        self,
    ) -> Contract:
        for milestone in self.payment_schedule:
            if not milestone["amount"]:
                multiplier = float(milestone["percentage"] * 0.01)
                amount = self.amount * multiplier
                milestone["amount"] = utils.format_num_2dec(amount)
        return self

    def get_contract_date(self) -> str:
        """gets contract date from given json"""
        if self.proposal_date["month"] < 10:
            return f"{self.proposal_date['year']}-0{self.proposal_date['month']}"
        else:
            return f"{self.proposal_date['year']}-{self.proposal_date['month']}"

    def get_cpi_base_date(self) -> str:
        """calculates base month for adjustment calculation"""
        if self.proposal_date["month"] == 1:
            base_year = self.proposal_date["year"] - 1
            base_month = 12
        else:
            base_year = self.proposal_date["year"]
            base_month = self.proposal_date["month"] - 1
        return f"{base_year}-{base_month}"

    def calculate_subtotal(
        self, milestones: list[int]
    ) -> float:  # TODO: FORMAT FLOAT 2decimals
        subtotal = 0
        for milestone in milestones:

            amount = self.payment_schedule[milestone]["amount"].replace(",", "")
            subtotal += float(amount)
        return subtotal
