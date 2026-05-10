import json
import typer
from pathlib import Path
from contract import Contract


def load_data(file_path: str):
    # from contract import Contract
    fp = Path(file_path)
    try:
        with open(fp, "r", encoding="utf8") as file:
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
            contract_amount=data["contract_amount"],
            currency=data["currency"],
            payment_schedule=data["payment_schedule"],
        )
    except FileNotFoundError:
        raise typer.BadParameter(f'File "{fp}" not found!')


def update_json(
    file_path: str,
    contract: Contract,
    milestones: list[int],
    billing_status: str,
) -> None:
    for milestone in milestones:
        if billing_status == "-b":
            contract.payment_schedule[milestone - 1]["billed"] = True
        elif billing_status == "-n":
            contract.payment_schedule[milestone - 1]["billed"] = False
    with open(file_path, "w", encoding="utf8") as file:
        json.dump(contract.__dict__, file, indent=2)
