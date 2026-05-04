from dataclasses import dataclass
import utils
from rich import print


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
    payment_schedule: list[dict[str, str | int | bool]]

    def print_contract(self) -> None:
        print(f"Selected contract: [yellow]{self.title}[/yellow]")

    def print_milestones(self) -> None:
        for i, milestone in enumerate(self.payment_schedule):
            print(f"[bold yellow][{i+1}]: [/bold yellow]", sep="", end=" ")
            for key, value in milestone.items():
                match key:
                    case "percentage":
                        print(f"[default]{value}% - [/default]", sep="", end=" ")
                    case "description":
                        print(value)
                    case "billed":
                        (
                            print("[green]Billed[/green]")
                            if value
                            else print("[red]Not billed[/red]")
                        )
            print()

    def calculate_milestone_amount(self) -> Contract:
        """
        calculates the amount of all contract's milestones
        """
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

    # def get_milestones(self) -> dict[str, str | int | bool]:
    #  return [milestone for milestone in self.paymentSchedule]
