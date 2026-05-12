import json
import typer
from pathlib import Path
from proforma_generator.contract import Contract
import os


def define_json_path(file: str, ENV_VAR_NAME: str) -> Path:
    name_to_json = f"{file}.json"
    dir = os.environ.get(ENV_VAR_NAME)
    fp = Path(str(dir)) / name_to_json
    return fp


def load_data(fp: Path):
    try:
        with open(fp, "r", encoding="utf8") as f:
            data = json.load(f)
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
    contract: Contract, milestones: list[int], billing_status: str, fp: Path
) -> None:
    for milestone in milestones:
        if billing_status == "b":
            contract.payment_schedule[milestone - 1]["billed"] = True
        elif billing_status == "n":
            contract.payment_schedule[milestone - 1]["billed"] = False
    with open(fp, "w", encoding="utf8") as f:
        json.dump(contract.__dict__, f, indent=2)
