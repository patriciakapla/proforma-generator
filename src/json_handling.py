import json
import typer
from pathlib import Path
from contract import Contract


def load_data(file_path: Path):
    # from contract import Contract

    try:
        with open(file_path, "r", encoding="utf8") as file:
            data = json.load(file)
        return Contract(
            contract_id=data["contract_id"],
            title=data["title"],
            client=data["client"],
            client_tax_id=data["client_tax_id"],
            client_project_manager=data["client_project_manager"],
            address=data["address"],
            proposal=data["proposal"],
            proposal_date=data["proposal_date"],
            amount=data["amount"],
            currency=data["currency"],
            payment_schedule=data["payment_schedule"],
        )
    except FileNotFoundError:
        raise typer.BadParameter(f'File "{file_path}" not found!')


def update_json(
    file_path: Path,
    contract: Contract,
    milestone: int | None = None,
    billed: bool | None = None,
) -> None:
    if not contract.payment_schedule[0]["amount"]:
        contract.calculate_milestone_amount()
        with open(file_path, "w", encoding="utf8") as file:
            json.dump(contract.__dict__, file, indent=2)
    if milestone:
        contract.payment_schedule[milestone]["billed"] = billed
        with open(file_path, "w", encoding="utf8") as file:
            json.dump(contract.__dict__, file, indent=2)
