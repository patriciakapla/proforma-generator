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
            contract_id=data["contractID"],
            title=data["title"],
            client=data["client"],
            client_tax_id=data["clientTaxID"],
            client_project_manager=data["clientProjectManager"],
            address=data["address"],
            proposal=data["proposal"],
            proposal_date=data["proposalDate"],
            contract_amount=data["contractAmount"],
            currency=data["currency"],
            payment_schedule=data["paymentSchedule"],
        )
    except FileNotFoundError:
        raise typer.BadParameter(f'File "{file_path}" not found!')


def update_json(
    file_path: Path,
    contract: Contract,
    milestone: int | None = None,
    billed: bool | None = None,
) -> None:
    if milestone:
        contract.payment_schedule[milestone]["billed"] = billed
        with open(file_path, "w", encoding="utf8") as file:
            json.dump(contract.__dict__, file, indent=2)
